import re, secrets


#TODO replace regex with a lexer that isnt pattern based ()
cxor_enable_string = re.compile('^[\s]*#pragma C3PO cxor(\(.+\))? enable')
cxor_disable_string = re.compile('^[\s]*#pragma C3PO cxor disable')
cxor_string = re.compile('^[\s]*#define ([a-zA-Z0-9_]+) "(.*)"')

shuffle_enable_string = re.compile('^[\s]*#pragma C3PO shuffle enable')
shuffle_case_string = re.compile('^[\s]*#pragma C3PO case')
shuffle_disable_string = re.compile('^[\s]*#pragma C3PO shuffle disable')

garbagestring = re.compile('^[\s]*#pragma C3PO garbage')

shatter_enable_string = re.compile('^[\s]*#pragma C3PO shatter(\(.+\))? enable( low| medium| high)?')
shatter_disable_string = re.compile('^[\s]*#pragma C3PO shatter disable')

mangle_enable_string = re.compile('^[\s]*#pragma C3PO mangle(\(.+\))? enable')
mangle_function_string = re.compile('([a-zA-Z_][a-zA-Z0-9_]*)\(')
mangle_disable_string = re.compile('^[\s]*#pragma C3PO mangle disable')

c3po_pragma_string = re.compile('^[\s]*#pragma C3PO (.*)')

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
        if c3po_pragma_string.match(self.cleanline):
            self.isflag = True
            #TODO set flags on and off and record a copy
            if cxor_enable_string.match(self.cleanline):
                if flags["cxor"]:
                    print("Duplicate cxor enable pragma found", file=sys.stderr)
                else:
                    flags["cxor"] = True
                    parts = cxor_enable_string.search(self.cleanline)
                    option = parts.group(1)
                    if option:
                        option = option.strip()[1:-1]
                        if option:
                            try:
                                flags["cxor_minlength"] = int(option)
                            except ValueError as ex:
                                print("Failed to parse padding optionue for cxor '{}' number was expected".format(option), file=sys.stderr)
            elif cxor_disable_string.match(self.cleanline):
                if not flags["cxor"]:
                    print("Unmatched cxor disable pragma found", file=sys.stderr)
                else:
                    flags["cxor"] = False
            elif shatter_enable_string.match(self.cleanline):
                if flags["shatter"]:
                    print("Duplicate shatter enable pragma found", file=sys.stderr)
                else:
                    flags["shatter"] = True
                    parts = shatter_enable_string.search(self.cleanline)
                    option = parts.group(1)
                    if option:
                        option = option.strip()[1:-1]
                        if option:
                            if option == "jmp":
                                flags["shatter_type"] = "jmp"
                            elif option == "call":
                                flags["shatter_type"] = "call"
                            else:
                                print("Unrecognized option for shatter type '{}' possible options: 'jmp','call'".format(option), file=sys.stderr)

                    level = parts.group(2).strip()
                    shatterer = 2
                    if level == "low":
                        shatterer = 3
                    elif level == "medium":
                        shatterer = 2
                    elif level == "high":
                        shatterer = 1
                    flags["shatter_level"] = shatterer

            elif shatter_disable_string.match(self.cleanline):
                if not flags["shatter"]:
                    print("Duplicate shatter disable pragma found", file=sys.stderr)
                else:
                    flags["shatter"] = False
            elif shuffle_enable_string.match(self.cleanline):
                if flags["shuffle"]:
                    print("Unmatched shuffle enable pragma found", file=sys.stderr)
                else:
                    flags["shuffle"] = True
                    shuffle.append([self.index, self.index, [[]]])
            elif shuffle_case_string.match(self.cleanline):
                shuffle[-1][1] = self.index
                shuffle[-1][2].append([])
                pass
            elif shuffle_disable_string.match(self.cleanline):
                if not flags["shuffle"]:
                    print("Unmatched shuffle disable pragma found", file=sys.stderr)
                else:
                    flags["shuffle"] = False
                    shuffle[-1][1] = self.index
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
