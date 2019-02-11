import re, secrets, sys, random


#TODO replace regex with a lexer that isnt pattern based ()
cxor_string = re.compile('^[\s]*#define ([a-zA-Z0-9_]+) "(.*)"')
#basically anything thats being called `asdf(` or `this_func (`
function_name = re.compile('([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*')
#i refuse to parse this
unsupported_function = re.compile('\(\s*\*[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*')
#c3po_common_match = re.compile('^[\s]*#pragma[\s]+c3po[\s]+([a-z]+)(\((.+)\))?[\s]*(.*)')
c3po_common_match = re.compile('^[\s]*#pragma[\s]+c3po(.*)$')

#asmlbl = """
#    __asm__(".shatter{0}:");
#"""

asmlbljmp = """
    __asm__(
        ".shatter{0}:"
        "xor %%eax, %%eax;"
        "test %%eax, %%eax;"
        "jz .done{0};"
        "{2} .shatter{1};"
        ".done{0}:"
        :::"%eax");"""# me, you, type

#turn foo(bar, baz) into ['bar', 'baz']
def param_edit(line, reorder=None):
    args = [""]
    preparams = True
    scope = 0
    passthrough = None
    trailing = ""
    for c in reversed(line):
        if passthrough:
            passthrough = c + passthrough
            continue
        if c == ')':
            scope += 1
            if scope == 1:
                trailing += ')'
                continue
        elif c == '(':
            scope -= 1
            if scope == 0:
                if reorder == None:
                    #just extract the args
                    return [arg.strip() for arg in reversed(args)]
                else:
                    #collapse reorder the params
                    newarray = []
                    for r in reorder:
                        newarray.append(args[len(args) - 1 - r].strip())
                    passthrough = '(' + ", ".join(newarray) + ''.join(c for c in reversed(trailing))
        if c == ',' and scope == 1:
            args.append("")
        elif scope > 0:
            args[-1] = c + args[-1]
        else:
            trailing += c

    if passthrough:
        return passthrough
    else:
        print("Failed to parse function '{}', is this valid c?".format(line), file=sys.stderr)

#turn directive1(opt1, opt2) directive2(opt1) into {"directive1":["opt1", "opt2"], "directive2":["opt1"]}
def pragma_split(line):
    directives = {}
    directive = ""
    option = ""
    scope = 0
    for c in line.strip():
        if c == ' ':
            if scope == 1:
                continue
            else:
                #no options for single flags
                directives[directive] = []

        if c == '(':
            scope += 1
            directives[directive] = [""]
            continue
        elif c == ')':
            scope -= 1
            directive = ""
            continue

        if scope == 0:
            directive += c
        elif scope == 1:
            if c == ',':
                directives[directive].append("")
            else:
                directives[directive][-1] += c
    return directives


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

def shatter(options, flags):
    for opt in options:
        if opt == "on":
            flags["cxor"] = True
        elif opt == "off":
            flags["cxor"] = False
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

def shuffle(options, flags, index, multiline):
    if "on" in options:
        flags["shuffle"] = True
        multiline["shuffle"].append([index, index, [[]]])
    elif "off" in options:
        flags["shuffle"] = False
        multiline["shuffle"][-1][1] = index
    else:
        print("Shuffle not turned on or off, unused directive", file=sys.stderr)

def mangle(options, feedforward):
    feedforward["mangle"] = True
    if "params" in options:
        feedforward["params"] = True
    if "name" in options:
        feedforward["name"] = True

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
        cmp = c3po_common_match.search(self.cleanline)
        if cmp:
            self.isflag = True
            pragma = pragma_split(cmp.group(1))
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

        #track every thing that gets called
        parts = function_name.search(self.cleanline)
        if parts and not unsupported_function.search(self.cleanline):
            func = parts.group(1)
            if func not in ["if", "while", "for"]:
                #this is a function mark it for resolution pass
                self.flags["func_mark"] = True

        #last feed checks are for next line affecting pragmas
        if "mangle" in lastfeed:
            self.flags["mangle"] = []
            #ensure the function is parsable
            parts = function_name.search(self.cleanline)
            if parts and not unsupported_function.search(self.cleanline):
                func = parts.group(1)
                if func not in ["if", "while", "for"]:
                    #log what operations to apply to fuinctions globally
                    if func not in multifile["mangle"]:
                        multifile["mangle"][func] = []

                    if "params" in lastfeed:
                        multifile["mangle"][func].append("params")
                        params = param_edit(self.cleanline)
                        multifile["mangle_params"][func] = [i for i,v in enumerate(params)]
                        random.shuffle(multifile["mangle_params"][func])
                    if "name" in lastfeed:
                        multifile["mangle"][func].append("name")
                        #TODO build the new name record it in the global func mangling table
            else:
                print("Unable to apply mangling to signature: '{}'".format(self.line), file=sys.stderr)
                print("Consider typedef for complex types", file=sys.stderr)


    def resolve(self, multiline, multifile, shatterself, shatterother):
        #shuffle params first
        for key, value in multifile["mangle_params"].items():
            if key in self.line:
                self.line = param_edit(self.line, value)
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

            key1array = list(secrets.token_bytes(len(string)))
            key2array = list(secrets.token_bytes(len(string)))
            #encrypt string with key
            newarray = [v ^ key1array[i] for i,v in enumerate(string)]
            #encrypt key with second key
            key1array = [v ^ key2array[i] for i,v in enumerate(key1array)]

            newarray.append(0)
            key1array.append(0)
            key2array.append(0)
            #this replaces the line so it must be before it
            self.line ="""//#define {1} "{0}"
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
        elif "shatter_mark" in self.flags and self.flags["shatter_mark"]:
            #build a shatter section
            self.line += asmlbljmp.format(shatterself[multiline["asm"]["index"]],
                                          shatterother[multiline["asm"]["index"]],
                                          self.flags["shatter_type"])
            multiline["asm"]["index"] += 1


    def write(self, file):
        if self.isflag:
            return
        else:
            file.write(self.line+"\n")
