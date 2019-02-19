from .file import File
import os
import secrets
import random
import json

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
            "encrypt_strings":{},
            #[function calls to be encrypted]
            "encrypt_functions":[],
            #to be encrypted after the encryption
            #[(key, length)]
            "post_encrypt":[],
        }
        #load all the files in one go just making sure they are c and real
        self.files = [File(index, os.path.join(srcpath, file), os.path.join(dstpath, file)) for index, file in enumerate(os.listdir(srcpath)) if os.path.isfile(os.path.join(srcpath, file)) and (file.endswith(".c") or file.endswith(".h"))]
        self.srcpath = srcpath
        self.dstpath = dstpath

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
        return

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
        total_len = len(key) + len(iv) + len(self.multifile["encrypt_functions"])*mode
        self.multifile["post_encrypt"].append({"key":key,"len":total_len})

        print(", ".join(chunked_key))
        print(", ".join(chunked_iv))
        #builtdata = '''{{{},
        #     {},
        #     {}}}'''.format("(void*)0x"+''.join("{:02x}".format(k) for i in range(int(len(key)/8)) for k in reversed(key[i*8:i*8+8])),
        #                                ", ".join("0x{:02x}".format(i) for i in iv),
        #                                ", ".join(self.multifile["encrypt_functions"]))

    #this actually writes the completed files
    def write(self):
        print("Writing:")
        for file in self.files:
            print("    {}".format(file))
            file.write()
        #write the state to the output folder
        with open(os.path.join(os.getcwd(), "c3po.json"), "w+") as cf:
            json.dump({"post_encrypt":self.multifile["post_encrypt"]}, cf)
