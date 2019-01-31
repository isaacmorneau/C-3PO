#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys, re, secrets, os
from random import shuffle, choice

cxor_enable_string = re.compile('^[\s]*#pragma C3PO cxor enable')
cxor_disable_string = re.compile('^[\s]*#pragma C3PO cxor disable')

simplestring = re.compile('^[\s]*#define ([a-zA-Z_]+) "(.*)"')

shufflestring = re.compile('^[\s]*#pragma C3PO shuffle')
optionstring = re.compile('^[\s]*#pragma C3PO option')
endstring = re.compile('^[\s]*#pragma C3PO end')

garbagestring = re.compile('^[\s]*#pragma C3PO garbage')

shatter_enable_string = re.compile('^[\s]*#pragma C3PO shatter enable( low| medium| high)?')
shatter_disable_string = re.compile('^[\s]*#pragma C3PO shatter disable')


def line_cxor(lines):
    parsedlines = []
    enabled = False
    for line in lines:
        cleanline = line.strip()

        #check for the pragmas
        if cxor_enable_string.match(cleanline):
            if enabled:
                print("Duplicate cxor enable pragma found", file=sys.stderr)
            enabled = True
            continue
        elif cxor_disable_string.match(cleanline):
            if not enabled:
                print("Duplicate cxor disable pragma found", file=sys.stderr)
            enabled = False
            continue

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
        print("Cxor enable pragma never closed", file=sys.stderr)
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

asmlbl = """
    __asm__(".shatter{0}:");
"""
asmlbljmp = """
    __asm__(
        "xor %%eax, %%eax;"
        "cmp %%eax, {0};"
        "jl .done{0};"
        "call .shatter{1};"
        ".done{0}:"
        :::"%eax");
"""

def line_garbage(lines):
    parsedlines = []
    enabled = False
    shatterer = 2
    labelnum = 0
    linenum = 0
    for line in lines:
        cleanline = line.strip()

        #check for the pragmas
        if shatter_enable_string.match(cleanline):
            if enabled:
                print("Duplicate shatter enable pragma found", file=sys.stderr)
            enabled = True
            linenum = 0
            parts = shatter_enable_string.search(cleanline)
            level = parts.group(1)
            if level == " low":
                shatterer = 3
            elif level == " high":
                shatterer = 1
            #elif level == " medium":
            else:
                shatterer = 2
            continue
        elif shatter_disable_string.match(cleanline):
            if not enabled:
                print("Duplicate shatter disable pragma found", file=sys.stderr)
            enabled = False
            continue

        #dont check when its not on
        #just pass the lines through
        if not enabled:
            parsedlines.append(line)
            continue

        #if garbagestring.match(cleanline):
        if linenum % shatterer == 0:
            #requesting
            labelnum += 1
            parsedlines.append(asmlbl.format(labelnum))
            parsedlines.append(asmlbljmp.format(labelnum, secrets.randbelow(labelnum) + 1))
        elif enabled:
            labelnum += 1
            parsedlines.append(asmlbl.format(labelnum))

        parsedlines.append(line)
        #counter for interspacing shatter
        linenum += 1

    if enabled:
        print("Shatter enable pragma never closed", file=sys.stderr)

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
                lines = line_cxor(lines)
                lines = line_shuffle(lines)
                lines = line_garbage(lines)

                for line in lines:
                    w.write(line)
