# -*- coding:utf-8 -*-

import sys

from minghu6.etc.cmd import auto_resume


def cli():
    auto_resume(sys.argv[1:])


if __name__ == '__main__':
    cli()