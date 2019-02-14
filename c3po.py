#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys
import os
from c3po.project import Project
from c3po.lex import LexTest
from c3po.file import FileTest
import unittest

if __name__ == "__main__":
    def print_help():
        print("usage: ./c3po.py /path/to/src /path/to/output <optional seed>")
        print("       ./c3po.py test")
        sys.exit(1)
    if len(sys.argv) == 1:
        print_help()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "test":
            suite = unittest.TestSuite()
            results = unittest.TestResult()
            suite.addTest(unittest.makeSuite(LexTest))
            suite.addTest(unittest.makeSuite(FileTest))
            runner = unittest.TextTestRunner()
            print(runner.run(suite))
        else:
            print_help()
    else:
        srcfolder = sys.argv[1]
        dstfolder = sys.argv[2]

        if not os.path.exists(dstfolder):
            os.mkdir(dstfolder)

        seed = None
        if len(sys.argv) == 4:
            seed = sys.argv[3]
        project = Project(srcfolder, dstfolder, seed)
        project.parse()
        project.resolve()
        project.write()

