#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
count file lines in dir
"""

import os

from argparse import ArgumentParser

from minghu6.etc.find import find


cnt_files = 0


def count_lines_file(fname, ignore_blank=False):
    with open(fname, 'rb') as fp:
        if ignore_blank:
            iterator = filter(lambda line: line.strip() !=
                              b'', fp)  # Warning: b'' != ''
        else:
            iterator = fp
        n = sum(1 for x in iterator)
    return n


def count_lines_dir(dir, exts=None, ignore_blank=False):
    """
    :param dir:
    :param ext:the file type which will be counted,
               default None means all type will be included
               you can customized by point a list for ext such as
               ['.py','.c','.cpp','.bat','.sh']

    :return:
    """
    global cnt_files
    n = 0
    new_exts = []
    for ext in exts:
        if ext.startswith("."):
            new_exts.append("*"+ext)
        else:
            new_exts.append(ext)

    # print(dir,ext,ignore_blank)
    for fullpath in find(new_exts, startdir=dir):
        cnt_files += 1
        n += count_lines_file(
            fullpath, ignore_blank
            )

    return n


def shell_interactive():
    parser = ArgumentParser(description='line counter')

    parser.add_argument('-p', '--path', dest='dir',
                        help='searched dir name')

    parser.add_argument('exts', metavar='.c .py',
                        nargs='*',
                        help=('file\'s ext type which will be searched\n'
                              '\tdefault all type'))

    parser.add_argument('-ib', '--ignore-blank', dest='ignore_blank',
                        action='store_true',
                        help='ignore blank lines during line count')

    args = parser.parse_args()

    if args.dir in (None, '.'):
        args.dir = os.path.abspath(os.path.curdir)

    return args


def cli():
    args = shell_interactive()
    n = count_lines_dir(
        dir=args.dir,
        exts=args.exts,
        ignore_blank=args.ignore_blank
    )

    print(f"counting: {cnt_files}")
    print(f"   total: {n}")


if __name__ == '__main__':
    cli()
