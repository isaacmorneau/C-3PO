from line import Line
import random, re

#lines with only whitespace
blankline = re.compile(r'^\s*$')
#multiline comments
multiline = re.compile(r'/\*.*?\*/', re.MULTILINE | re.DOTALL)
#singleline comments and trailing white space
lineextra = re.compile(r'\s*(//.*)?$')
#shouldn't join the last line
trueline = re.compile(r'^.*[){;}\\]$')
#someone uses alman style
shittyline = re.compile(r'\s*{')
#includes and pragmas
pragmaline = re.compile(r'^\s*#.*$')
#cleanup lines that will be joined
prejoin = re.compile(r'^\s*(?=\s)')

def simplify(fulldata):
    simplelines = []
    joining = False
    for line in multiline.sub("", fulldata).split("\n"):
        stripped = lineextra.sub("", line, 1)
        if not blankline.match(stripped):
            if shittyline.match(stripped):
                simplelines[-1] += prejoin.sub("", stripped, 1)
                joining = False
            elif trueline.match(stripped) or pragmaline.match(stripped):
                if joining:
                    simplelines[-1] += prejoin.sub("", stripped, 1)
                    joining = False
                else:
                    simplelines.append(stripped)
            else:
                if joining:
                    simplelines[-1] += prejoin.sub("", stripped, 1)
                else:
                    simplelines.append(stripped)
                    joining = True
    return simplelines

class File():
    def __init__(self, index, srcpath, dstpath):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.index = index

        #structure
        #shuffle [
        #   (start, end, [[lines],[lines]])
        #]

        self.multiline = {
            "asm": {
                "total":0,
                "index":0,
                "indexes":[],
            },
            "shuffle":[],
            "mangle":[],
            "mangle_match":{},
        }

        self.flags = {
            "cxor":False,
            "shatter":False,
            "shuffle":False,
            "mangle":False,
            "shatter_level":2,
            "shatter_type":"call",
        }


        with open(srcpath) as f:
            self.lines = [Line(index, line) for index, line in enumerate(simplify(f.read()))]

    def __str__(self):
        return "[{}:{}]".format(len(self.lines), self.srcpath)

    def classify(self, multifile):
        for line in self.lines:
            line.classify(self.flags, self.multiline, multifile)

    def resolve(self, multifile):
        #this collapses the shuffled lines before the rest of resolution
        for shuffle in self.multiline["shuffle"]:
            random.shuffle(shuffle[2])
            #replace the lines that were shuffled
            self.lines[shuffle[0]:shuffle[1]] = [line for chunk in shuffle[2] for line in chunk]

        #ensure every option is used by doing a cheap shuffle to operate like a true
        #uniform distributioin
        me = list(self.multiline["asm"]["indexes"])
        random.shuffle(me)
        you = list(self.multiline["asm"]["indexes"])
        random.shuffle(you)

        #reset index back down
        self.multiline["asm"]["index"] = 0

        for line in self.lines:
            line.resolve(self.multiline, multifile, me, you)

    def write(self):
        with open(self.dstpath, "w") as f:
            for line in self.lines:
                line.write(f)
