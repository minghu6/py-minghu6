# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import sys

from minghu6.algs.operator import getitem
from minghu6.etc.echo import echo


def interactive():
    echo(getitem(sys.argv, 1, ''))


if __name__ == '__main__':
    interactive()
