#!/usr/bin/env python3
#TODO make sure the version is at least 3.6 for secrets

import sys, os

from project import Project

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: ./c3po.py /path/to/src /path/to/output")
        sys.exit(1)
    srcfolder = sys.argv[1]
    dstfolder = sys.argv[2]

    if not os.path.exists(dstfolder):
        os.mkdir(dstfolder)

    project = Project(srcfolder, dstfolder)
    project.parse()
    project.resolve()
    project.write()

