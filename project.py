from file import File
import os

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
        #load all the files in one go just making sure they are c and real
        self.files = [File(index, os.path.join(srcpath, file), os.path.join(dstpath, file)) for index, file in enumerate(os.listdir(srcpath)) if os.path.isfile(os.path.join(srcpath, file)) and (file.endswith(".c") or file.endswith(".h"))]
        #TODO at some point do incremental builds
        #for file in files:
        #    if not os.path.exists(file[2]) or os.path.getmtime(file[1]) > os.path.getmtime(file[2]):

    #this performs the inital tokenization and collection of info
    #this will find the positions for future resolution
    def parse(self):
        print("Parsing:")
        for file in self.files:
            print("    {}".format(file))
            file.classify()

    #this will now chose what should be resolved in things such as the
    #asm labels to be chosen globally
    def resolve(self):
        print("Resolving:")
        for file in self.files:
            print("    {}".format(file))
            file.resolve()

    #this actually writes the completed files
    def write(self):
        print("Writing:")
        for file in self.files:
            print("    {}".format(file))
            file.write()