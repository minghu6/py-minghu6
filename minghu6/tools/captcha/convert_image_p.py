# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import os
import sys

from PIL import Image
from minghu6.text.color import color


def main(n, ext):
    n = int(n)
    for i in range(n):
        # path = sys.stdin.readline().strip() #encoding pointed already
        path = input().strip()
        newpath = path + ext
        try:
            with Image.open(path) as img_obj:
                img_obj.save(newpath)
            os.remove(path)
        except Exception as ex:
            color.print_err(ex)

        color.print_ok('fetched %s.    no.%d' % (newpath, i + 1))


if __name__ == '__main__':
    main(*sys.argv[1:])
