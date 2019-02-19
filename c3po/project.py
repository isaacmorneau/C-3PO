from .file import File
import os
import secrets
import random

c3po_face ="""\033[33;m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢙⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠛⠁⢀⣼⡷⠈⠓⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⢛⣩⠴⢒⡂⠀⣠⡀⠀⠀⠀⠀⠢⣍⡛⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⢟⣡⡞⠉⢠⣾⠟⠁⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣷⣦⡙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⢋⣴⣿⣿⣤⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣷⡍⢦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⡞⡱⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⣆⠀⠀⠀⠀⠀
⠀⠀⠀⢠⠏⡼⣽⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⢦⠀⠀⠀⠀
⠀⠀⢠⡟⠘⢸⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⡆⠀⠀⠀
⠀⠀⣼⠀⠀⣿⣿⣿⣿⣁⠄⠀⠀⢀⣀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⢻⡀⠀⠀
⠀⠀⡏⢀⢼⣿⣿⣿⣋⣵⣾⣿⣿⣾⣭⣉⡛⠦⠀⠐⠛⣡⣶⣿⣿⣿⣿⣯⣛⢿⣿⣿⣿⣿⣿⡿⡟⡇⠀⠀
⠀⢰⡇⢸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⣶⣿⣿⣿⡿⡿⣿⣿⣿⣿⣷⣹⣿⣿⣿⣿⡇⡀⡇⠀⠀
⠀⢸⡇⣼⣿⡿⣃⣿⣿⠟⠁⢀⣀⠀⠉⣿⣿⡿⢀⡿⣿⣿⡟⠁⠁⠉⠋⢿⠀⣠⠿⠻⣿⣿⣿⡇⡷⡇⠀⠀
⠀⣸⡇⣿⣿⣾⣿⣿⣸⡀⠀⠘⠿⠀⢠⢿⣿⣿⣸⠟⠂⢻⠇⠀⠺⠿⠀⢸⠀⣷⣶⣦⣬⡻⣿⣄⠀⡇⠀⠀
⢸⣷⠂⣿⠁⢸⣿⣿⣷⡳⢄⣀⣀⠠⠊⣼⣿⠇⢹⡀⠀⠈⢣⡀⠀⠀⢀⠞⣰⣿⣿⣿⣿⣿⣧⣿⣶⢿⠀⠀
⢸⡇⠀⢹⠀⢸⣿⣿⣿⣧⡀⠀⠀⠀⠀⡼⠋⠀⢸⡷⢄⠀⢀⣨⣭⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⠀⠀
⠀⣷⡄⢸⡄⠸⣿⣿⠸⣿⣿⣦⣀⣠⣾⣷⣾⣶⣿⣿⣶⣤⣼⣿⣿⣿⣿⣿⢹⣿⢿⣿⣿⣿⣿⣇⡎⡇⠀⠀
⠀⢻⠁⠘⡇⠀⣿⣿⡆⣿⣿⣿⣿⣿⣿⡿⠋⠁⢉⢻⣿⣿⠏⠉⣴⣿⣿⠃⡟⢸⣿⣿⣿⣿⡿⢻⣿⡇⠀⠀
⠀⠈⢳⡄⣧⠀⢿⣿⣧⠸⣿⣿⣿⣿⡟⠀⠀⠀⠘⣷⣿⣯⣴⣾⣿⣿⠃⢸⠇⢸⢿⣿⣿⣿⣿⣾⠉⠀⠀⠀
⠀⠀⠀⣧⢸⡀⢸⣿⣿⡄⢿⣿⣿⣿⣿⣶⣦⣤⣶⣶⣿⣿⣿⣿⣿⠃⠀⣾⠀⣾⢸⣿⣿⣿⣷⡇⠀⠀⠀⠀
⠀⠀⠀⠸⡄⠃⠀⢿⣿⣧⠬⣿⣷⣾⣏⣛⣛⣛⣛⣛⣫⣿⣿⣿⡝⠒⢰⠷⠦⣿⣼⣿⢿⡿⠿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⣽⣷⡀⠈⣿⣿⡄⠹⣿⣿⣿⣿⡇⠀⢾⣿⣿⣿⣿⣿⠀⠀⡾⠀⠀⣶⣿⡏⣼⡿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣍⣧⠀⢻⣿⣿⠀⢿⣿⡿⣿⣄⠀⣸⣿⣿⣟⣿⠏⠀⢸⡇⠀⣸⣿⣿⢁⡟⣁⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣼⣿⡆⠘⣿⣿⣷⣼⣿⣿⣿⠟⢼⣻⣿⠟⢉⣡⣴⣶⣿⣇⢀⣿⣿⣏⣼⡇⢹⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡛⠛⠛⢉⣽⣿⣏⣩⣿⣿⣿⣿⣿⣿⣿⣷⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⢻⣭⣭⣭⣭⣭⣭⣽⡛⠿⢿⣿⣿⣿⣿⣿⣍⠙⢛⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⡇⣿⣿⣿⣿⣿⣿⣷⣶⡶⠒⠂⠘⠿⣿⣿⣿⣶⣶⣶⣾⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣇⣛⣛⣛⣛⣛⣛⣛⣛⣛⣃⣀⣀⣀⣀⣀⣀⣈⣉⣉⣛⣛⣛⣛⣛⣻⡏
 -------------------------------------
      C PrePreProcessor Obfuscator\033[;m"""

class Project():
    def __init__(self, srcpath, dstpath, seed=None):
        #we need repeatability
        if not seed:
            seed = "".join("{:02x}".format(t) for t in secrets.token_bytes(5))

        print("Using seed: {}".format(seed))
        random.seed(seed)

        #print(c3po)

        self.files = []

        self.multifile = {
            #function name: [list of operations]
            "mangle":{},
            #function name: replacement name
            "mangle_match":{},
            #function name: [shuffle order of params]
            "mangle_params":{},
            #[functions to be variadically mangled]
            "mangle_variadic":[],
            #token name: [padded string bytes]
            "encrypt":{},
            #to be encrypted after the encryption
            #[(key, length)]
            "post_encrypt":[],
        }
        #load all the files in one go just making sure they are c and real
        self.files = [File(index, os.path.join(srcpath, file), os.path.join(dstpath, file)) for index, file in enumerate(os.listdir(srcpath)) if os.path.isfile(os.path.join(srcpath, file)) and (file.endswith(".c") or file.endswith(".h"))]

    #this performs the inital tokenization and collection of info
    #this will find the positions for future resolution
    def parse(self):
        print("Parsing:")
        for file in self.files:
            print("    {}".format(file))
            file.classify(self.multifile)
        #mangle to match ida or binja labels
        for func, ops in self.multifile["mangle"].items():
            if "name" in ops:
                self.multifile["mangle_match"][func+"("] = "sub_"+"".join("{:02x}".format(t) for t in [random.randint(0, 256) for i in range(2)])+"("

    #this will now chose what should be resolved in things such as the
    #asm labels to be chosen globally
    def resolve(self):
        print("Resolving:")
        for file in self.files:
            print("    {}".format(file))
            file.resolve(self.multifile)
        if len(self.multifile["mangle"]) > 0:
            print("Functions mangled:")
        for func,opts in self.multifile["mangle"].items():
            print("    [{}".format(func), end="")
            if "name" in opts:
                print(" : {}".format(self.multifile["mangle_match"][func+"("][:-1]), end="")
            if "shuffle" in opts:
                print(" : {}".format(self.multifile["mangle_params"][func]), end="")
            if "variadic" in opts:
                print(" : <variadic>", end="")
            print("]")

    #this actually writes the completed files
    def write(self):
        print("Writing:")
        for file in self.files:
            print("    {}".format(file))
            file.write()
