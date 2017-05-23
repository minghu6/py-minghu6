# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""GREP

Usage:
  grep -i=<input-pattern> <file-pattern>... [-l]

Options:
  -i=<input-pattern>  input pattern to search (regex match)
  <file-pattern>      file to search (fnmatch)
  -l                  list detail information

"""
import minghu6
# TODO http://stackoverflow.com/questions/26659142/cat-grep-and-cut-translated-to-python
from docopt import docopt
from minghu6.etc.shell_tools import grep


def main(i, file_patterns, l=False):
    for result in grep(i, file_patterns):
        if l:
            print('%s %d' % (result.path, result.line))
            print(result.content)
        else:
            print(result.content)


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    i = arguments['-i']
    file_patterns = arguments['<file-pattern>']
    l = arguments['-l']
    main(i, file_patterns, l)


if __name__ == '__main__':
    cli()
