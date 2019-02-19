import os
import json

class PostProcess():
    def __init__(self, binarypath, statepath):
        self.binarypath = binarypath
        with open(statepath, "r") as s:
            self.state = json.load(s)
        self.binaryfile = open(self.binarypath,"wb+")

    def __del__(self):
        self.binaryfile.close()

    def encrypt(self):
        for batch in self.state["post_encrypt"]:
            print("finding {}:{}".format(batch["len"],batch["key"]))
