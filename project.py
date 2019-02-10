from file import File
import os, secrets

class Project():
    def __init__(self, srcpath, dstpath):
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
        self.files = []

        self.multifile = {
            #function name: [list of operations]
            "mangle":{},
            #function name: replacement name
            "mangle_match":{},
            #function name: [shuffle order of params]
            "mangle_params":{},
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
                self.multifile["mangle_match"][func+"("] = "sub_"+"".join("{:02x}".format(t) for t in secrets.token_bytes(2))+"("
            if "params" in ops:
                #TODO actually parse and generate a shuffle order
                #this is also where a variadic functions should be added
                print("func {}".format(func))

    #this will now chose what should be resolved in things such as the
    #asm labels to be chosen globally
    def resolve(self):
        print("Resolving:")
        for file in self.files:
            print("    {}".format(file))
            file.resolve(self.multifile)
        if len(self.multifile["mangle"]) > 0:
            print("Functions mangled:")
        for func,new in self.multifile["mangle_match"].items():
            print("    [{} : {}]".format(func[:-1], new[:-1]))

    #this actually writes the completed files
    def write(self):
        print("Writing:")
        for file in self.files:
            print("    {}".format(file))
            file.write()
