import re
import sys
import random
from .lex import *
from .asm import *

#the usage between cleanline and line is that cleanline checks are faster but line should be used to preserve formatting

asmlbljmp = '''
    __asm__(
        ".shatter{0}:"
        "xor %%eax, %%eax;"
        "test %%eax, %%eax;"
        "jz .done{0};"
        "{2} .shatter{1};"
        ".done{0}:"
        :::"%eax");'''

def broken_bytes():
    #select command then option within it
    ops = random.choice(random.choice(everyopt))
    return '''
        __asm__(
            {}
            :::);'''.format('\n            '.join("\".byte 0x{:x};\"".format(opt) for opt in ops))


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

def encrypt(options, feedforward):
    feedforward["encrypt"] = True
    feedforward["mode"] = "aes"
    for opt in options:
        if opt == "aes":
            feedforward["mode"] = "aes"
            #no other modes supported yet
        else:
            try:
                feedforward["padding"] = int(opt)
            except ValueError as ex:
                print("Unrecognized option for encrypt: '{}'".format(opt), file=sys.stderr)

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
        #TODO add directive to disable all c3po processing of a set of lines
        #otherwise double includes and stuff like itb wont function correctly

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
                    if directive == "shatter":
                        shatter(options, flags)

                    elif directive == "shuffle":
                        shuffle(options, flags, self.index, multiline)
                    elif directive == "case":
                        multiline["shuffle"][-1][2].append([])

                    elif directive == "mangle":
                        mangle(options, feedforward)

                    elif directive == "encrypt":
                        encrypt(options, feedforward)

                    else:
                        print("Unrecognized directive '{}'".format(directive), file=sys.stderr)
        elif is_include(self.cleanline):
            self.isflag = True
            include = get_include(self.cleanline)
            if include not in multiline["includes"]:
                multiline["includes"].append(include)
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
        if "encrypt" in lastfeed:
            if is_string_define(self.cleanline):
                self.flags["encrypt_mark"] = "string"

                token, value = get_string_define(self.cleanline)
                if "padding" in lastfeed:
                    value.extend(0 for i in range(lastfeed["padding"]))
                if token not in multifile["encrypt_strings"]:
                    #[string with null termination][PKCS7 padding]
                    padding = 16 - len(value) % 16
                    #always pad
                    if padding > 0:
                        value.extend(padding for i in range(padding))
                    else:
                        value.extend(16 for i in range(16))
                    multifile["encrypt_strings"][token] = value
            elif is_function(self.cleanline):
                self.flags["encrypt_mark"] = "func"
                func = get_function_calls(self.cleanline)[0]
                if is_defdec(self.cleanline):
                    if func not in multifile["encrypt_functions"]:
                        #[string with null termination][PKCS7 padding]
                        multifile["encrypt_functions"].append(func)
                else:
                    print("can only tag function declarations for encryption: '{}'".format(self.cleanline), file=sys.stderr)
            else:
                print("Cannot encrypt requested type: '{}'".format(self.cleanline), file=sys.stderr)

    def resolve(self, multiline, multifile, shatterself, shatterother):
        for token, value in multifile["encrypt_strings"].items():
            if token in self.cleanline and not is_string_define(self.cleanline):
                #AES 256 requires 32 byte key lengths
                key = list(bytes([random.randrange(0, 256) for i in range(32)]))
                iv = list(bytes([random.randrange(0, 256) for i in range(16)]))
                builtdata = '''{{{},
             {},
             {}}}'''.format(", ".join("0x{:02x}".format(k) for k in key),
                                        ", ".join("0x{:02x}".format(i) for i in iv),
                                        ", ".join("0x{:02x}".format(v) for v in value))
                multifile["post_encrypt"].append({"key":key,"len":len(value)})
                if "<stdint.h>" not in multiline["includes"]:
                    multiline["includes"].append("<stdint.h>")
                if "\"c3po.h\"" not in multiline["includes"]:
                    multiline["includes"].append("\"c3po.h\"")
                self.line = """
    {{
        static volatile uint8_t _{0}_data[] = {1};
        uint8_t* _{0}_key = (uint8_t*)_{0}_data;
        uint8_t* _{0}_iv = (uint8_t*)_{0}_data + 32;
        uint8_t* _{0}_enc = (uint8_t*)_{0}_data + 48;

        struct AES_ctx ctx;
        AES_init_ctx_iv(&ctx, _{0}_key, _{0}_iv);
        AES_CBC_decrypt_buffer(&ctx, _{0}_enc, {2});

        //TODO verify padding
        char* {0} = (char*)_{0}_enc;
        {3}
    }}
""".format(token, builtdata, len(value), self.cleanline)
                #a bit extreme but its needed so that internal functions can still mangle generated calls
                self.cleanline = self.line.strip()
        #for func in multifile["encrypt_functions"]:
        #    if func in self.cleanline and not is_defdec(self.cleanline):
        #TODO add the function decrypton code here

        if "shatter_mark" in self.flags and self.flags["shatter_mark"]:
            #build a shatter section
            self.line += asmlbljmp.format(shatterself[multiline["asm"]["index"]],
                                          shatterother[multiline["asm"]["index"]],
                                          self.flags["shatter_type"])
            multiline["asm"]["index"] += 1

        if "assert_mark" in self.flags:
            args = ", ".join(get_function_arguments("assert", self.cleanline))

            if "<stdbool.h>" not in multiline["includes"]:
                multiline["includes"].append("<stdbool.h>")
            self.line = '''    {{
        volatile bool assert_check =!({});
        if (assert_check) {{'''.format(args)

            #TODO collect any asm nasties to troll the disassembler in here
            self.line += broken_bytes()
            self.line += "\n        }\n    }"

        if "encrypt_mark" in self.flags:
            if self.flags["encrypt_mark"] == "string":
                self.line = "//the following constant is included encrypted inline\n//"+self.cleanline
            #dont comment out function definitions
        #shuffle params first
        for key, value in multifile["mangle_params"].items():
            if key in self.cleanline:
                self.line = reorder_arguments(key, value, self.line)
        for func in multifile["mangle_variadic"]:
            if func in self.cleanline:
                try:
                    arguments = get_function_arguments(func, self.cleanline)
                except Exception:
                    continue

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
                    if "<stdarg.h>" not in multiline["includes"]:
                        multiline["includes"].append("<stdarg.h>")
                    self.line += """
    va_list va;
    va_start(va, {});
    va_end(va);
""".format(finalnamed)
                else:
                    #TODO allow randomization to be configurable
                    additional_args = [str(random.randrange(0, 65535)) for i in range(random.randrange(1, 10))]
                    self.line = append_arguments(func, additional_args, self.line)
        #name mangling should happen after as generated code from previous resolution may need to be mangled
        #break all the names
        for key, value in multifile["mangle_match"].items():
            if key in self.cleanline:
                self.line = self.line.replace(key, value)
                self.cleanline = self.cleanline.replace(key, value)

    def write(self, file):
        if self.isflag:
            return
        else:
            file.write(self.line+"\n")
