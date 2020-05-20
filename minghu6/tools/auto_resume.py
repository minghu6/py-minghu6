# -*- coding:utf-8 -*-

import sys

from minghu6.etc.cmd import auto_resume


def cli():
    name = '-'.join(sys.argv[1]) + '.log'
    auto_resume(sys.argv[1:], name=name)


if __name__ == '__main__':
    cli()