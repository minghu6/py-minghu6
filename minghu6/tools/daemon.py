# -*- coding:utf-8 -*-

import sys

from minghu6.etc.cmd import daemon

def cli():
    daemon(sys.argv[1:])


if __name__ == '__main__':
    cli()

