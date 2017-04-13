# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from argparse import ArgumentParser
import os
import sys

from minghu6.etc import fileformat
from minghu6.algs.dict import remove_key, remove_value
from minghu6.text.color import color

def main_img(path, ext, outdir=os.path.curdir):
    fileformat.convert_img(path, ext=ext, outdir=outdir)

def main_info(path):

    name = fileformat.fileformat(path)
    if name == fileformat.UNKNOWN_TYPE:
        color.print_err(name)
    else:
        color.print_info('%s<===>%s'%(name.normal_name, name.ext_name))



def cli():
    parser_main = ArgumentParser()
    parser_main.set_defaults(func=parser_main.print_usage)
    sub_parsers = parser_main.add_subparsers(help='sub-command')


    # main_parser


    # sub_parser: img
    parser_img = sub_parsers.add_parser('image', help='convert image file format')

    parser_img.add_argument('path', nargs='?', help='image file path')
    parser_img.add_argument('-o', '--outdir', help='output directory')
    parser_img.add_argument('-ext', '--ext',
                            help='to this format like png gif ...')

    parser_img.set_defaults(func=main_img)


    # sub_parser: info
    parser_info = sub_parsers.add_parser('info', help='recognise file format')
    parser_info.add_argument('path', nargs='?', help='file path')

    parser_info.set_defaults(func=main_info)

    parse_result = parser_main.parse_args()
    args = remove_value(remove_key(parse_result.__dict__, 'func'), None)
    try:
        parse_result.func(**args)
    except Exception as ex:
        color.print_err(type(ex), ex)
        color.print_err('Invalid args')


if __name__ == '__main__':

    cli()