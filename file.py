from line import Line
import random

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
            "mangle":False,
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
