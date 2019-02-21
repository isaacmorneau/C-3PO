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
            #[function calls to be encrypted]
            "encrypt_functions":[],
            "encrypt_len":0,
        }

        #for additional out of line data
        self.prelines = []
        self.postlines = []

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

        #TODO enable this
        if self.multiline["encrypt_functions"]:
            key = list(bytes([random.randrange(0, 256) for i in range(32)]))
            iv = list(bytes([random.randrange(0, 256) for i in range(16)]))

            #bytes per pointer
            x64 = 8
            x86 = 4
            #TODO this is assuming 64 bit pointers, allow the config of both
            mode = x64
            #breaks up the raw bytes into endian appropriate 32 or 64 bit chunks
            chunked_key = ["(void*)0x"+''.join("{:02x}".format(c) for c in reversed(key[i*mode:i*mode+mode])) for i in range(int(len(key)/mode))]
            chunked_iv = ["(void*)0x"+''.join("{:02x}".format(c) for c in reversed(iv[i*mode:i*mode+mode])) for i in range(int(len(iv)/mode))]
            #encode how much space the function pointers will take up
            total_len = len(key) + len(iv) + len(self.multiline["encrypt_functions"])*mode
            padding = 16 - total_len % 16
            pkc = None
            #always pad
            if padding > 0:
                pkc = [padding for i in range(padding)]
                total_len += padding
            else:
                pkc = [16 for i in range(16)]
                total_len += 16
            chunked_pkc = ["(void*)0x"+''.join("{:02x}".format(c) for c in reversed(pkc[i*mode:i*mode+mode])) for i in range(int(len(pkc)/mode))]


            multifile["post_encrypt"].append({"key":key,"len":total_len})
            self.multiline["encrypt_len"] = total_len

            built_struct = '''{{{},
        {},
        {},
        {}}}'''.format(", ".join(chunked_key),
                       ", ".join(chunked_iv),
                       ", ".join(chunk["func"] for chunk in self.multiline["encrypt_functions"]),
                       ", ".join(chunked_pkc))

            header = '''
static volatile void * volatile c3po_functions_map[];
'''
            self.prelines.append(header)

            file = '''
static volatile void * volatile c3po_functions_map[] = {};
'''.format(built_struct)
            self.postlines.append(file)

        for line in self.lines:
            line.resolve(self.multiline, multifile, me, you)

    def write(self):
        with open(self.dstpath, "w") as f:
            for include in sorted(self.multiline["includes"]):
                f.write("#include {}\n".format(include))
            if self.prelines:
                f.write("\n".join(self.prelines))
            for line in self.lines:
                line.write(f)
            if self.postlines:
                f.write("\n".join(self.postlines))
