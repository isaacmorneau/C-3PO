#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys, re, secrets, os
from random import shuffle, choice

enablestring = re.compile('^[\s]?#pragma C3PO enable')
disablestring = re.compile('^[\s]?#pragma C3PO disable')

simplestring = re.compile('^[\s]?#define ([a-zA-Z_]+) "(.*)"')

shufflestring = re.compile('^[\s]?#pragma C3PO shuffle')
optionstring = re.compile('^[\s]?#pragma C3PO option')
endstring = re.compile('^[\s]?#pragma C3PO end')

garbagestring = re.compile('^[\s]?#pragma C3PO garbage')


def line_string_xor(lines):
    parsedlines = []
    enabled = False
    for line in lines:
        cleanline = line.strip()

        #check for the pragmas
        if enablestring.match(cleanline):
            if enabled:
                print("Duplicate enable pragma found", file=sys.stderr)
            enabled = True
        elif disablestring.match(cleanline):
            if not enabled:
                print("Duplicate disable pragma found", file=sys.stderr)
            enabled = False

        #dont check when its not on
        if not enabled:
            parsedlines.append(line)
            continue

        #check if this is something to change
        if simplestring.match(cleanline):
            parts = simplestring.search(cleanline)
            varname = parts.group(1)
            original = parts.group(2)
            #magic to parse escapes
            #thanks jerub https://stackoverflow.com/a/4020824
            string = bytes(original, "utf-8").decode("unicode_escape").encode()
            encarray = list(secrets.token_bytes(len(string)))
            newarray = []
            for i in range(len(string)):
                newarray.append(encarray[i] ^ string[i])

            newarray.append(0)
            encarray.append(0)
            parsedlines.append("""//#define {1} "{0}"
#define {1}_ENC {{{3},{4}}}
#define {1}_LEN {2}
""".format(original, varname, len(newarray), ','.join(hex(e) for e in newarray), ','.join(hex(e) for e in encarray)))
        else:
            #maintain unchanged lines
            parsedlines.append(line)

    #check for bad formatting
    if enabled:
        print("Enable pragma never closed", file=sys.stderr)
    return parsedlines

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

        elif optionstring.match(cleanline):
            if not shuffling:
                print("Option pragma found without shuffle", file=sys.stderr)
                continue
            shuffle_sets.append([])

        elif endstring.match(cleanline):
            if not shuffling:
                print("End pragma found without shuffle", file=sys.stderr)
                continue
            shuffle(shuffle_sets)
            for shuff in shuffle_sets:
                for s in shuff:
                    parsedlines.append(s)
            shuffling = False

        elif shuffling:
            shuffle_sets[-1].append(line)

        else:
            parsedlines.append(line)
    if shuffling:
        print("Missing end pragma", file=sys.stderr)
        #this should not be relied on but this allows it to not fatal on bad definitons
        for shuff in shuffle_sets:
            for s in shuff:
                parsedlines.append(s)

    return parsedlines

asmgarbage = """
    __asm__(
        ".intel_syntax;"
        ".start{0}:"
{1}
        ".done{0}:"
        ".att_syntax;"
        :{2}
        :{3}
        :{4}
    );
"""

def asm_gt():
    h = secrets.randbelow(255) + 1

    opts =["""
"xor %%eax, %%eax;"
"cmp %%eax, {0};"
"""]

    return choice(opts).format(hex(h))

def asm_garbage(labelnum):
    return asmgarbage.format(labelnum,
"""
{0}
"jnz .done{1};"
"jmp .heh{2};"
""".format(asm_gt(), labelnum, choice([1,2,3])),
                             "",
                             "",
                             '"%eax"')

def line_garbage(lines):
    parsedlines = []
    labelnum = 0
    for line in lines:
        cleanline = line.strip()
        if garbagestring.match(cleanline):
            labelnum += 1
            parsedlines.append(asm_garbage(labelnum))
        else:
            parsedlines.append(line)

    return parsedlines


if __name__ == "__main__":
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

    if len(sys.argv) != 3:
        print("usage: ./c3po.py /path/to/src /path/to/output")
        sys.exit(1)
    srcfolder = sys.argv[1]
    outfolder = sys.argv[2]

    files = [(file, os.path.join(srcfolder, file), os.path.join(outfolder, file)) for file in os.listdir(srcfolder) if os.path.isfile(os.path.join(srcfolder, file)) and (file.endswith(".c") or file.endswith(".h"))]

    for file in files:
        if not os.path.exists(file[2]) or os.path.getmtime(file[1]) > os.path.getmtime(file[2]):
            print("PrePreProcessing {}".format(file[0]))
            with open(file[1], "r") as r, open(file[2], "w") as w:
                lines = r.readlines()
                lines = line_string_xor(lines)
                lines = line_garbage(lines)
                liens = line_shuffle(lines)

                for line in lines:
                    w.write(line)
