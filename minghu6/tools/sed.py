# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""SED

Usage:
  sed <cmd> <stream>

Options:
  <cmd>
  <stream>
"""
import minghu6
from docopt import docopt
from minghu6.etc.shell_tools import sed


def main(stream, cmd):
    return sed(stream, cmd)


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    stream = arguments['<stream>']
    cmd = arguments['<cmd>']
    main(stream, cmd)


if __name__ == '__main__':
    cli()
