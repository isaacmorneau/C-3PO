#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys
import os
import argparse
import c3po.output
from c3po.project import Project
from c3po.lex import LexTest
from c3po.file import FileTest
from c3po.post import PostProcess, PostTest
import unittest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C3PO - C PrePreProcessor Obfuscator")
    parser.add_argument("type", help="select the operational mode", choices=['build','post','test'])
    parser.add_argument("-s","--source", help="build, post: the path to the folder to parse from", nargs=1)
    parser.add_argument("-o","--output", help="build only: the path to the folder to output to", nargs=1)
    parser.add_argument("--json", help="post only: path to the json state", nargs=1)
    parser.add_argument("--seed", help="build only: random seed", nargs=1)
    parser.add_argument("--quiet", help="suppress output", action="store_true")

    args = parser.parse_args()

    if args.quiet:
        c3po.output.verbose = False

    if args.json and args.type != 'post':
        parser.error("--json option is only for post mode")
    if args.seed and args.type != 'build':
        parser.error("--seed option is only for build mode")

    if args.type == 'post':
        if not args.source:
            parser.error("--source option required for build")
    elif args.type == 'build':
        if not args.source:
            parser.error("--source option required for build")
        if not args.output:
            parser.error("--output option required for build")
    elif args.type == 'test':
        if args.source:
            parser.error("--source option ignored on test")
        elif args.output:
            parser.error("--output option ignored on test")

    if args.type == 'test':
        suite = unittest.TestSuite()
        results = unittest.TestResult()
        suite.addTest(unittest.makeSuite(LexTest))
        suite.addTest(unittest.makeSuite(FileTest))
        suite.addTest(unittest.makeSuite(PostTest))
        runner = unittest.TextTestRunner()
        print(runner.run(suite))
    elif args.type == 'post':
        statepath = None
        if not args.json:
            basefolder = os.path.dirname(args.source[0])
            statepath = os.path.join(basefolder, "c3po.json")
        else:
            statepath = args.json[0]
        post = PostProcess()
        post.read_data(args.source[0])
        post.read_state(statepath)
        post.encrypt()
        post.write(args.source[0])

    elif args.type == 'build':
        srcfolder = args.source[0]
        dstfolder = args.output[0]

        if not os.path.exists(dstfolder):
            os.mkdir(dstfolder)

        seed = None
        if args.seed:
            seed = args.seed[0]
        project = Project(srcfolder, dstfolder, seed)
        project.parse()
        project.resolve()
        project.write()

