#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
Return all files matching a filename pattern at and below a root directory;

custom version of the now deprecated find module in the standard library:

find() is a generator that uses the os.walk() generator to yield just
matching filenames: use findlist() to force results list generation;
################################################################################
"""

import fnmatch, os
import re
def find(pattern, startdir=os.curdir, regex_match=False):
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        for name in subsHere + filesHere:
            if regex_match and re.fullmatch(pattern, name) is not None:
                pass
            elif fnmatch.fnmatch(name, pattern):
                pass
            else:
                continue

            fullpath = os.path.join(thisDir, name)
            yield fullpath


def findlist(pattern, startdir=os.curdir, dosort=False, regex_match=False):
    matches = list(find(pattern, startdir, regex_match=regex_match))
    if dosort: matches.sort()
    return matches

if __name__ == '__main__':
    import sys
    namepattern, startdir = sys.argv[1], sys.argv[2]
    for name in find(namepattern, startdir): print(name)
