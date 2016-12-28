#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
count file lines in dir
"""

import sys
import os

from argparse import ArgumentParser


def count_lines_file(fname):

    with open(fname,'rb') as fp:
        n=(sum(1 for x in fp))

    return n

def count_lines_dir(dir,ext=None):
    """

    :param dir:
    :param ext:the file type which will be counted,
               default None means all type will be included
               you can customized by point a list for ext such as ['.py','.c','.cpp','.bat','.sh']

    :return:
    """
    n=0
    print(dir,ext)
    for rootdir,subdirs,files in os.walk(dir):

        for name in files:
            if (ext==None) or (os.path.splitext(name)[1] in ext):

                n+=count_lines_file(os.path.join(rootdir,name))



    return n

def shell_interactive():
    parser=ArgumentParser()

    parser.add_argument('-p','--path',dest='dir',
                        help='searched dir name')

    parser.add_argument('ext',metavar='.c .py',
                        nargs='*',
                        help=('file\'s ext type which will be searched\n'
                              '\tdefault all type'))

    args=parser.parse_args()

    if args.dir in (None,'.'):
        args.dir=os.path.abspath(os.path.curdir)
    if args.ext == []:
        args.ext=None

    return args

def interactive():

    args=shell_interactive()
    n=count_lines_dir(dir=args.dir,ext=args.ext)
    print(n)

if __name__ == '__main__':
    interactive()































