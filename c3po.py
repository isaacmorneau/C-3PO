#!/usr/bin/env python3

import sys, re, secrets, os

simplestring = re.compile('#define ([a-zA-Z_]+) "(.*)"')


def string_obfuscation(lines):
    parsedlines = []

    for line in lines:
        cleanline = line.strip()
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
                stringparsed_lines = string_obfuscation(lines)

                for line in stringparsed_lines:
                    w.write(line)
