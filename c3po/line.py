import re
import sys
import random
from .lex import *

#the usage between cleanline and line is that cleanline checks are faster but line should be used to preserve formatting

#TODO replace regex with a lexer that isnt pattern based ()
cxor_string = re.compile('^[\s]*#define ([a-zA-Z0-9_]+) "(.*)"')

#asmlbl = """
#    __asm__(".shatter{0}:");
#"""

asmlbljmp = '''
    __asm__(
        ".shatter{0}:"
        "xor %%eax, %%eax;"
        "test %%eax, %%eax;"
        "jz .done{0};"
        "{2} .shatter{1};"
        ".done{0}:"
        :::"%eax");'''


broken_options = [
    #jmp
    [0x7f],
    [0x74],
    #mov
    [0x89,0x84,0xd9],
    [0x48,0x89,0x44,0x24],
    [0x64,0x48,0x8b,0x04],
    [0x64,0x48,0x8b,0x04,0x25],
    #shr
    [0xc0,0xe8],
    #vmovaps
    [0xc5,0xf8,0x29,0x44,0x24],
    #lea
    [0x48,0x8d,0x44,0x24],
    #xor
    [0x64,0x48,0x33,0x04,0x25],
]

def broken_bytes():
    ops = random.choice(broken_options)
    return '''
        __asm__(
            {}
            :::);'''.format('\n            '.join("\".byte 0x{:x};\"".format(opt) for opt in ops))


#functions to parse each directive
def cxor(options, flags):
    for opt in options:
        if opt == "on":
            flags["cxor"] = True
        elif opt == "off":
            flags["cxor"] = False
        else:
            try:
                flags["cxor_minlength"] = int(opt)
            except ValueError as ex:
                print("Failed to parse padding optionue for cxor '{}' number was expected".format(opt), file=sys.stderr)
    if len(options) == 0:
        print("Cxor not turned on or off, unused directive", file=sys.stderr)

def shatter(options, flags):
    for opt in options:
        if opt == "on":
            flags["shatter"] = True
        elif opt == "off":
            flags["shatter"] = False
        elif opt == "jmp":
            flags["shatter_type"] = "jmp"
        elif opt == "call":
            flags["shatter_type"] = "call"
        elif opt == "low":
            flags["shatter_level"] = 3
        elif opt == "medium":
            flags["shatter_level"] = 2
        elif opt == "high":
            flags["shatter_level"] = 1
        else:
            print("Unrecognized option for shatter: '{}'".format(opt), file=sys.stderr)
    if len(options) == 0:
        print("Shatter  not turned on or off, unused directive", file=sys.stderr)

def shuffle(options, flags, index, multiline):
    for opt in options:
        if "on" in options:
            flags["shuffle"] = True
            multiline["shuffle"].append([index, index, [[]]])
        elif "off" in options:
            flags["shuffle"] = False
            multiline["shuffle"][-1][1] = index
        else:
            print("Unrecognized option for shuffle: '{}'".format(opt), file=sys.stderr)
    if len(options) == 0:
        print("Shuffle not turned on or off, unused directive", file=sys.stderr)


def mangle(options, feedforward):
    feedforward["mangle"] = True
    for opt in options:
        if "shuffle" == opt:
            feedforward["shuffle"] = True
        elif "name" == opt:
            feedforward["name"] = True
        elif "variadic" == opt:
            feedforward["variadic"] = True
        else:
            print("Unrecognized option for mangle: '{}'".format(opt), file=sys.stderr)
    if len(options) == 0:
        #TODO decide what the default behavior for mangle
        pass

class Line():
    def __init__(self, index, rawline):
        self.line = rawline
        self.cleanline = rawline.strip()
        self.flags = {}
        #this is a flag of some kind, it should not be output
        self.isflag = False
        self.index = index

    def __str__(self):
        return "{}:{}:{}".format(self.index, self.flags.items(), self.cleanline)

    def classify(self, flags, multiline, multifile, lastfeed):
        feedforward = {}
        #do all pragama matches first
        if is_c3po_pragma(self.cleanline):
            if "assert" in self.cleanline:
                #early exit as its replacing the line not signalling the future
                self.flags = dict(flags)
                self.flags["assert_mark"] = True
                return feedforward
            else:
                self.isflag = True
                pragma = pragma_split(self.cleanline)
                for directive, options in pragma.items():
                    if directive == "cxor":
                        cxor(options, flags)
                    elif directive == "shatter":
                        shatter(options, flags)
                    elif directive == "shuffle":
                        shuffle(options, flags, self.index, multiline)
                    elif directive == "case":
                        multiline["shuffle"][-1][2].append([])
                    elif directive == "mangle":
                        mangle(options, feedforward)
                    else:
                        print("Unrecognized directive '{}'".format(directive), file=sys.stderr)
        #copy the state we set
        self.flags = dict(flags)

        #mark lines for future resolution
        #this is for multiline blocks as well not for single line pragmas
        if not self.isflag:
            self.flagless_line(lastfeed, multiline, multifile)
        return feedforward

    def flagless_line(self, lastfeed, multiline, multifile):
        if self.flags["shuffle"]:
            multiline["shuffle"][-1][2][-1].append(self)

        if self.flags["shatter"]:
            multiline["asm"]["total"] += 1

        #if we are in shatter mode tag lines that need to be replaced
        if self.flags["shatter"] and self.index % self.flags["shatter_level"] == 0:
            self.flags["shatter_mark"] = True
            multiline["asm"]["indexes"].append(multiline["asm"]["index"])
            multiline["asm"]["index"] += 1

        if self.flags["cxor"] and cxor_string.match(self.cleanline):
            self.flags["cxor_mark"] = True

        #last feed checks are for next line affecting pragmas
        if "mangle" in lastfeed:
            self.flags["mangle"] = []
            #ensure the function is parsable
            functions = get_function_calls(self.cleanline)
            if len(functions) == 1:
                func = functions[0]
                if func not in multifile["mangle"]:
                    multifile["mangle"][func] = []
                if "shuffle" in lastfeed:
                    args = get_function_arguments(func, self.cleanline)
                    #this extra check is to make sure variadic functions still work
                    params = [i for i in range(len(args))]
                    if is_variadic(args):
                        if len(args) > 2:
                            #theres no point of shuffling if theres only one position
                            #dont mess with variadic functions last 2
                            params = params[:-2]
                            random.shuffle(params)
                            multifile["mangle_params"][func] = params
                            multifile["mangle"][func].append("shuffle")
                        else:
                            print("Not enough arguments to make shuffling useful: '{}'".format(self.cleanline), file=sys.stderr)
                    else:
                        random.shuffle(params)
                        multifile["mangle_params"][func] = params
                        multifile["mangle"][func].append("shuffle")
                if "name" in lastfeed:
                    #build the new name record it in the global func mangling table
                    multifile["mangle"][func].append("name")
                if "variadic" in lastfeed:
                    args = get_function_arguments(func, self.cleanline)
                    if is_variadic(args):
                        print("Function already variadic, unable to apply mangling to signature: '{}'".format(self.cleanline), file=sys.stderr)
                    elif is_defdec(self.cleanline):
                        if func not in multifile["mangle_variadic"]:
                            multifile["mangle_variadic"].append(func)
                        multifile["mangle"][func].append("variadic")
                        #TODO append the va start and end to the line make sure its not optimized out
                        #additioinal checks for if this is a definition or a declaration are required
                    else:
                        print("Can only apply mangling to function definitions and declarations: '{}'".format(self.cleanline), file=sys.stderr)

            else:
                print("Unable to apply mangling to signature: '{}'".format(self.cleanline), file=sys.stderr)


    def resolve(self, multiline, multifile, shatterself, shatterother):
        #shuffle params first
        for key, value in multifile["mangle_params"].items():
            if key in self.cleanline:
                self.line = reorder_arguments(key, value, self.line)
        for func in multifile["mangle_variadic"]:
            if func in self.cleanline:
                arguments = get_function_arguments(func, self.cleanline)

                if len(arguments) == 0:
                    #you need at least one named param so ensure there is one
                    if is_defdec(self.cleanline):
                        self.line = append_arguments(func, ["int base"], self.line)
                        self.cleanline = append_arguments(func, ["int base"], self.cleanline)
                        arguments.append("int base")
                    else:
                        self.line = append_arguments(func, ["0"], self.line)
                        self.cleanline = append_arguments(func, ["0"], self.cleanline)
                        arguments.append("0")

                if is_defdec(self.cleanline, [";"]):
                    self.line = append_arguments(func, ["..."], self.line)
                elif is_defdec(self.cleanline,["{"]):
                    self.line = append_arguments(func, ["..."], self.line)
                    #quick break to select the name
                    argument_names = get_token_names(arguments)
                    finalnamed = argument_names[-1].split()[-1]
                    self.line += """
    va_list va;
    va_start(va, {});
    va_end(va);
""".format(finalnamed)
                else:
                    #TODO allow randomization to be configurable
                    additional_args = [str(random.randrange(0, 65535)) for i in range(random.randrange(1, 10))]
                    self.line = append_arguments(func, additional_args, self.line)
        #break all the names
        for key, value in multifile["mangle_match"].items():
            if key in self.line:
                self.line = self.line.replace(key, value)


        if "cxor_mark" in self.flags and self.flags["cxor_mark"]:
            parts = cxor_string.search(self.cleanline)
            varname = parts.group(1)
            original = parts.group(2)
            #magic to parse escapes
            #thanks jerub https://stackoverflow.com/a/4020824
            string = bytes(original, "utf-8").decode("unicode_escape").encode()

            #handle requested padding of strings
            if "cxor_minlength" in self.flags:
                if self.flags["cxor_minlength"] > len(string):
                    string += bytes([0 for i in range(self.flags["cxor_minlength"] - len(string))])

            key1array = list(bytes([random.randrange(0, 256) for i in range(len(string))]))
            key2array = list(bytes([random.randrange(0, 256) for i in range(len(string))]))
            #encrypt string with key
            newarray = [v ^ key1array[i] for i,v in enumerate(string)]
            #encrypt key with second key
            key1array = [v ^ key2array[i] for i,v in enumerate(key1array)]

            newarray.append(0)
            key1array.append(0)
            key2array.append(0)
            #this replaces the line so it must be before it
            self.line = """//#define {1} "{0}"
#define {1}_ENC {{{3}}}
#define {1}_KEY1 {{{4}}}
#define {1}_KEY2 {{{5}}}
#define {1}_LEN {2}""".format(original,
                              varname,
                              len(newarray),
                              ','.join(hex(e) for e in newarray),
                              ','.join(hex(e) for e in key1array),
                              ','.join(hex(e) for e in key2array)
                              )
        if "shatter_mark" in self.flags and self.flags["shatter_mark"]:
            #build a shatter section
            self.line += asmlbljmp.format(shatterself[multiline["asm"]["index"]],
                                          shatterother[multiline["asm"]["index"]],
                                          self.flags["shatter_type"])
            multiline["asm"]["index"] += 1
        if "assert_mark" in self.flags:
            args = ", ".join(get_function_arguments("assert", self.cleanline))
            self.line = "    if(!({})) {{".format(args)
            #TODO collect any asm nasties to troll the disassembler in here
            self.line += broken_bytes()
            self.line += "\n    }"




    def write(self, file):
        if self.isflag:
            return
        else:
            file.write(self.line+"\n")
