# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""path2uuid
convert file name to uuid name(exclude its ext)
Usage:
  path2uuid <pattern> [-d]

Options:
  <pattern>        file pattern to match such as "abc*.mp4"
  [-d]             restore the path (exclude ext name)

"""
import fnmatch
import os

import minghu6
from docopt import docopt
from minghu6.etc.path2uuid import path2uuid
from color import color


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    pattern = arguments['<pattern>']

    for fn in os.listdir(os.curdir):
        if fn == '.path2uuid.sqlite3':
            continue
        if fnmatch.fnmatch(fn, pattern) or fn == pattern:
            res = path2uuid(fn, d=arguments['-d'])

            if res is None:
                color.print_info('%s Do nothing' % fn)
            else:
                color.print_ok('convert %s to %s' % (fn, res))


if __name__ == '__main__':
    cli()
