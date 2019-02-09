from line import Line
import random, re

blankline = re.compile(r'^\s*$')
multiline = re.compile(r'/\*.*?\*/', re.MULTILINE | re.DOTALL)
comment = re.compile(r'\s*//.*')
trailingwhite = re.compile(r'\s*$')
trueline = re.compile(r'[{;]$')
def simplify(fulldata):
    simplelines = []
    for line in multiline.sub("", fulldata).split("\n"):
        stripped = trailingwhite("", comment.sub("", line, 1), 1)
        if not blankline.match(stripped):
            print(stripped)
            simplelines.append(stripped)
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
