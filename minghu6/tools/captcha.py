# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.graphic.captcha import preprocessing as pp
from minghu6.graphic.captcha import recognise as rg
from minghu6.graphic.captcha.get_image import get_image
from minghu6.algs.dict import remove_key, remove_value
from PIL import Image
from argparse import ArgumentParser
import os

split_method_set = {'bisect'   : pp.bisect_img,
                    'boxsplit' : pp.boxsplit_img}

recognise_method_set = {'tesseract' : rg.tesseract}

def main_split(path, num=None, split_method='bisect', outdir=os.path.curdir):
    #path, n=None, split_method='bisect', outdir=os.path.curdir

    assert split_method in split_method_set, 'split_method do not exist!'

    assert num!=None or split_method != 'bisect','bisect method need the param n'
    split_method = split_method_set[split_method]

    if os.path.isfile(path):
        imgObj_file_name, ext = os.path.splitext(os.path.basename(path))
        if ext == '':
            ext = '.gif'

        with Image.open(path) as imgObj:
            box_img = split_method(imgObj, n=num)
    else:
        imgObj=get_image(path)
        box_img = split_method(imgObj, n=num)
        imgObj_file_name, ext = 'captcha', '.gif'

    # base_path = os.path.join(outdir, os.path.basename(path))
    for i, sub_img in enumerate(box_img):

        sub_img_path = os.path.join(outdir,
                                    imgObj_file_name+'_{0:d}'.format(i)+ext)
        sub_img.save(sub_img_path, ext[1:])


def main_recognise(path, recognise_method='tesseract'):

    assert recognise_method in recognise_method_set, 'recognise_method do not exist'
    recognise_method = recognise_method_set[recognise_method]
    try:
        result = recognise_method(path)
    except Exception as ex:
        print(ex)
    else:
        print(result, len(result))


def main(args):
    print(args)
    pass


def interactive():
    parser_main = ArgumentParser()
    sub_parsers = parser_main.add_subparsers(help='sub-command')


    # main_parser

    # sub_parser: split
    parser_split = sub_parsers.add_parser('split', help='split the image')
    parser_split.add_argument('path', nargs='?', help='image file path(exclude image url)')
    parser_split.add_argument('-n', '--num', type=int,
                              help='point the number of char of img')

    parser_split.add_argument('-split', '--split_method',
                              choices=['bisect', 'boxsplit'],
                              help='split method (default bisect)')

    parser_split.add_argument('-o', '--outdir', help='output directory')
    parser_split.set_defaults(func=main_split)


    # sub_parser: recognise
    parser_recognise = sub_parsers.add_parser('recognise',
                                              help='recognise the captcha')

    parser_recognise.add_argument('path', nargs='?', help='image file path(exclude image url)')
    parser_recognise.add_argument('-recognise', '--recognise_method',
                              choices=['tesseract'],
                              help='recognise method (default tesseract)')

    parser_recognise.set_defaults(func=main_recognise)



    parse_result = parser_main.parse_args()
    args = remove_value(remove_key(parse_result.__dict__, 'func'), None)
    parse_result.func(**args)




if __name__ == '__main__':
    interactive()