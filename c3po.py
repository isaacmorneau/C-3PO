#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys, re, secrets, os, random

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

c3po_pragma_string = re.compile('^[\s]*#pragma C3PO (.*)')


class Project():
    def __init__(self, srcpath, dstpath):
        print("""
            /~\\
           |o o)  C-3PO
           _\=/_
      #   /  _  \   #
       \\\\//|/.\|\\\\//
        \/  \_/  \/
           |\ /|
           \_ _/
           | | |
           | | |
           []|[]
           | | |
    ______/_]_[_\______
     C PrePreProcessor
        Obfuscator""")
        self.files = []
        #load all the files in one go just making sure they are c and real
        self.files = [File(index, os.path.join(srcfolder, file), os.path.join(dstfolder, file)) for index, file in enumerate(os.listdir(srcfolder)) if os.path.isfile(os.path.join(srcfolder, file)) and (file.endswith(".c") or file.endswith(".h"))]
        #TODO at some point do incremental builds
        #for file in files:
        #    if not os.path.exists(file[2]) or os.path.getmtime(file[1]) > os.path.getmtime(file[2]):

    #this performs the inital tokenization and collection of info
    #this will find the positions for future resolution
    def parse(self):
        print("Parsing:")
        for file in self.files:
            print("    {}".format(file))
            file.classify()

    #this will now chose what should be resolved in things such as the
    #asm labels to be chosen globally
    def resolve(self):
        print("Resolving:")
        for file in self.files:
            print("    {}".format(file))
            file.resolve()

    #this actually writes the completed files
    def write(self):
        print("Writing:")
        for file in self.files:
            print("    {}".format(file))
            file.write()


class File():
    def __init__(self, index, srcpath, dstpath):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.index = index

        self.asm_state = {
            "total":0,
            "index":0,
            "indexes":[],
        }

            #structure
            #shuffle [
            #   (start, end, [[lines],[lines]])
            #]
        self.shuffle = []

        self.flags = {
            "cxor":False,
            "shatter":False,
            "shuffle":False,
            "shatter_level":2,
            "shatter_type":"call",
        }


        with open(srcpath) as f:
            self.lines = [Line(index, line) for index, line in enumerate(f.readlines())]

    def __str__(self):
        return "[{}:{}]".format(len(self.lines), self.srcpath)

    def classify(self):
        for line in self.lines:
            line.classify(self.asm_state, self.flags, self.shuffle)

    def resolve(self):
        #this collapses the shuffled lines before the rest of resolution
        for shuffle in self.shuffle:
            random.shuffle(shuffle[2])
            #replace the lines that were shuffled
            self.lines[shuffle[0]:shuffle[1]] = [line for chunk in shuffle[2] for line in chunk]

        #ensure every option is used by doing a cheap shuffle to operate like a true
        #uniform distributioin
        me = list(self.asm_state["indexes"])
        random.shuffle(me)
        you = list(self.asm_state["indexes"])
        random.shuffle(you)

        #reset index back down
        self.asm_state["index"] = 0

        for line in self.lines:
            line.resolve(self.asm_state, me, you)

    def write(self):
        with open(self.dstpath, "w") as f:
            for line in self.lines:
                line.write(f)


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

def line_shuffle(lines):
    parsedlines = []
    shuffle_sets = [[]]
    shuffling = False

    for line in lines:
        cleanline = line.strip()

        if shufflestring.match(cleanline):
            if shuffling:
                print("Duplicate shuffle pragma found", file=sys.stderr)
                continue
            shuffle_sets = [[]]
            shuffling = True
            continue

        elif optionstring.match(cleanline):
            if not shuffling:
                print("Option pragma found without shuffle", file=sys.stderr)
                continue
            shuffle_sets.append([])
            continue

        elif endstring.match(cleanline):
            if not shuffling:
                print("End pragma found without shuffle", file=sys.stderr)
                continue
            shuffling = False
            shuffle(shuffle_sets)
            for shuff in shuffle_sets:
                for s in shuff:
                    parsedlines.append(s)
            continue

        elif shuffling:
            shuffle_sets[-1].append(line)
        else:
            parsedlines.append(line)

    if shuffling:
        print("Shuffle end pragma never closed", file=sys.stderr)
        #this should not be relied on but this allows it to not fatal on bad definitons
        for shuff in shuffle_sets:
            for s in shuff:
                parsedlines.append(s)

    return parsedlines

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: ./c3po.py /path/to/src /path/to/output")
        sys.exit(1)
    srcfolder = sys.argv[1]
    dstfolder = sys.argv[2]

    if not os.path.exists(dstfolder):
        os.mkdir(dstfolder)

    project = Project(srcfolder, dstfolder)
    project.parse()
    project.resolve()
    project.write()

