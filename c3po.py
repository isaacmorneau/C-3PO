#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys
import os
from c3po.project import Project
from c3po.lex import LexTest
from c3po.file import FileTest
from c3po.post import PostProcess
import unittest

if __name__ == "__main__":
    def print_help():
        print("usage: ./c3po.py build /path/to/src /path/to/output <optional seed>")
        print("       ./c3po.py post /path/to/binary <optional state json path>")
        print("       ./c3po.py test")
        sys.exit(1)
    if len(sys.argv) == 1:
        print_help()
    elif sys.argv[1] == "test":
        suite = unittest.TestSuite()
        results = unittest.TestResult()
        suite.addTest(unittest.makeSuite(LexTest))
        suite.addTest(unittest.makeSuite(FileTest))
        runner = unittest.TextTestRunner()
        print(runner.run(suite))
    elif sys.argv[1] == "post":
        statepath = None
        if len(sys.argv) == 3:
            basefolder = os.path.dirname(sys.argv[2])
            statepath = os.path.join(basefolder, "c3po.json")
        else:
            statepath = sys.argv[3]
        post = PostProcess(sys.argv[2], statepath)
        post.encrypt()
        post.write()

    elif sys.argv[1] == "build":
        srcfolder = sys.argv[2]
        dstfolder = sys.argv[3]

        if not os.path.exists(dstfolder):
            os.mkdir(dstfolder)

        seed = None
        if len(sys.argv) == 5:
            seed = sys.argv[4]
        project = Project(srcfolder, dstfolder, seed)
        project.parse()
        project.resolve()
        project.write()

