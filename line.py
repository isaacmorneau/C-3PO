import re, secrets, sys


#TODO replace regex with a lexer that isnt pattern based ()
cxor_string = re.compile('^[\s]*#define ([a-zA-Z0-9_]+) "(.*)"')
mangle_function_string = re.compile('.*[\s]+([a-zA-Z_][a-zA-Z0-9_]*)\(.*')

c3po_common_match = re.compile('^[\s]*#pragma[\s]+c3po[\s]+([a-z]+)(\((.+)\))?[\s]*(.*)')

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

def state_matcher(line):
    parts = c3po_common_match.search(line)
    name = parts.group(1)
    tmp = parts.group(3)
    options = []
    if tmp:
        options = [opt.strip() for opt in tmp.split(",")]
    toggle = parts.group(4)
    return name, options, toggle

def flag_toggle(name, toggle, flags):
    if name in ["cxor", "shatter", "shuffle", "mangle"]:
        if toggle == "enable":
            if flags[name]:
                print("Duplicate pragma, {} is enabled".format(name), file=sys.stderr)
            else:
                flags[name] = True
                return True
        elif toggle == "disable":
            if not flags[name]:
                print("Unmatched pragma, {} is disabled".format(name), file=sys.stderr)
            else:
                flags[name] = False
                return False
    return

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

    def classify(self, flags, multiline, multifile):
        #do all pragama matches first
        if c3po_common_match.match(self.cleanline):
            self.isflag = True

            name, options, toggle = state_matcher(self.cleanline)

            is_toggle = flag_toggle(name, toggle, flags)

            if is_toggle == True:
                if name == "cxor" and len(options) > 0:
                    try:
                        flags["cxor_minlength"] = int(options[0])
                    except ValueError as ex:
                        print("Failed to parse padding optionue for cxor '{}' number was expected".format(options[0]), file=sys.stderr)
                if name == "shatter":
                    for opt in options:
                        if opt == "jmp":
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
                if name == "shuffle":
                    multiline["shuffle"].append([self.index, self.index, [[]]])
            elif is_toggle == False:
                if name == "shuffle":
                    multiline["shuffle"][-1][1] = self.index
            elif name == "case":
                multiline["shuffle"][-1][2].append([])
            else:
                print("Unrecognized option '{}'".format(self.cleanline))
        #copy the state we set
        self.flags = dict(flags)

        #mark lines for future resolution
        if not self.isflag:
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
            if self.flags["mangle"] and mangle_function_string.match(self.cleanline):
                parts = mangle_function_string.search(self.cleanline)
                func = parts.group(1)
                self.flags["mangle_mark"] = func
                if func not in multifile["mangle"]:
                    multifile["mangle"].append(func)

    def resolve(self, multiline, multifile, shatterself, shatterother):
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
