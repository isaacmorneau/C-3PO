import re, secrets, sys


#TODO replace regex with a lexer that isnt pattern based ()
cxor_string = re.compile('^[\s]*#define ([a-zA-Z0-9_]+) "(.*)"')
mangle_function_string = re.compile('([a-zA-Z_][a-zA-Z0-9_]*)\(')

c3po_common_match = re.compile('^[\s]*#pragma[\s]+C3PO[\s]+([a-z]+)(\((.+)\))?[\s]*(.*)')

#asmlbl = """
#    __asm__(".shatter{0}:");
#"""

asmlbljmp = """
    __asm__(
        "xor %%eax, %%eax;"
        "call .shatter{2};"
        "inc %%eax;"
        "cmp %%eax, 0;"
        "jg .done{1};"
        "{0} .shatter{2};"
        ".shatter{1}:"
        "mov %%eax, {1};"
        "ret;"
        ".done{1}:"
        :::"%eax");
"""# type, me, you

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

    def classify(self, asm_state, flags, shuffle):
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
                    shuffle.append([self.index, self.index, [[]]])
            elif is_toggle == False:
                if name == "shuffle":
                    shuffle[-1][1] = self.index
            elif name == "case":
                shuffle[-1][2].append([])
            else:
                print("Unrecognized option '{}'".format(self.cleanline))
        #copy the state we set
        self.flags = dict(flags)

        #mark lines for future resolution
        if not self.isflag:
            if self.flags["shuffle"]:
                shuffle[-1][2][-1].append(self)

            if self.flags["shatter"]:
                asm_state["total"] += 1

            #if we are in shatter mode tag lines that need to be replaced
            if self.flags["shatter"] and self.index % self.flags["shatter_level"] == 0:
                self.flags["shatter_mark"] = True
                asm_state["indexes"].append(asm_state["index"])
                asm_state["index"] += 1

            if self.flags["cxor"] and cxor_string.match(self.cleanline):
                self.flags["cxor_mark"] = True

    def resolve(self, asm_state, shatterself, shatterother):
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

            encarray = list(secrets.token_bytes(len(string)))
            newarray = []
            for i in range(len(string)):
                newarray.append(encarray[i] ^ string[i])

            newarray.append(0)
            encarray.append(0)
            #this replaces the line so it must be before it
            self.line ="""//#define {1} "{0}"\n#define {1}_ENC {{{3},{4}}}\n#define {1}_LEN {2}""".format(
                original, varname, len(newarray), ','.join(hex(e) for e in newarray), ','.join(hex(e) for e in encarray))
        elif "shatter_mark" in self.flags and self.flags["shatter_mark"]:
            #build a shatter section
            self.line += asmlbljmp.format(self.flags["shatter_type"],
                                          shatterself[asm_state["index"]],
                                          shatterother[asm_state["index"]])
            asm_state["index"] += 1

    def write(self, file):
        if self.isflag:
            return
        else:
            file.write(self.line)
