# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import os
import re
from collections import namedtuple
from fnmatch import fnmatch

from minghu6.etc.filecharset import guess_charset

GrepResultTuple = namedtuple('GrepResultTuple', ['content', 'path', 'line'])


def grep(pattern, file_patterns, startdir=os.curdir):
    for (thisDir, _subsHere, filesHere) in os.walk(startdir):
        for name in filesHere:
            fullpath = os.path.join(thisDir, name)
            if os.path.isfile(fullpath) and any([fnmatch(name, file_pattern) for file_pattern in file_patterns]):
                result = guess_charset(open(fullpath, 'rb'))
                if result is None: continue
                encoding = result['encoding']
                if encoding is None:
                    encoding = 'latin-1'
                for i, line in enumerate(open(fullpath, 'rb')):
                    line = line.decode(encoding, 'ignore')
                    if re.search(pattern, line) is not None:
                        yield GrepResultTuple(line, name, i + 1)
