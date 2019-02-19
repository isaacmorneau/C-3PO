from .line import Line
import random
import re
import unittest

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

class FileTest(unittest.TestCase):
    def test_simplify(self):
        self.assertEqual('\n'.join(simplify(
"""int scoper(int s, int v)
{
    //so much
    (void)v;/* garbage */
    return s;
}""")),"""int scoper(int s, int v){
    (void)v;
    return s;
}""")

class File():
    def __init__(self, index, srcpath, dstpath):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.index = index

        #structure
        #shuffle [
        #   (start, end, [[lines],[lines]])
        #]

        #multiline single file block post resolution options
        self.multiline = {
            "asm": {
                "total":0,
                "index":0,
                "indexes":[],
            },
            "shuffle":[],
            "includes":[],
        }

        #multiline single file block options
        self.flags = {
            "cxor":False,
            "shatter":False,
            "shuffle":False,
            "shatter_level":2,
            "shatter_type":"call",
        }


        with open(srcpath) as f:
            self.lines = [Line(index, line) for index, line in enumerate(simplify(f.read()))]

    def __str__(self):
        return "[{}:{}]".format(len(self.lines), self.srcpath)

    def classify(self, multifile):
        forward = {}
        for line in self.lines:
            forward = line.classify(self.flags, self.multiline, multifile, forward)

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
            for include in sorted(self.multiline["includes"]):
                f.write("#include {}\n".format(include))
            for line in self.lines:
                line.write(f)
