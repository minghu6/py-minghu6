# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.graphic.captcha import preprocessing as pp
from minghu6.graphic.captcha import recognise as rg
from minghu6.graphic.captcha.get_image import get_image

import  minghu6.graphic.captcha.train as train_m

from minghu6.algs.dict import remove_key, remove_value
from minghu6.etc.path import add_postfix

from minghu6.text.color import color

from PIL import Image
from argparse import ArgumentParser
import os

preprocessing_method_dict = {'binary'      : pp.binary_img,
                             'clear_noise' : pp.clearNoise_img,
                             'sharpen'     : pp.sharpen_img,
                             'remove_frame':pp.removeFrame_img}


split_method_dict = {'bisect'   : pp.bisect_img,
                    'boxsplit' : pp.boxsplit_img}

recognise_method_dict = {'tesseract' : rg.tesseract}

PREPROCESSING_FLAG_DICT = {'binary'       : 'b',
                           'clear_noise'  : 'cln',
                           'sharpen'      : 'shp',
                           'remove_frame' : 'rf'} # output image name postfix


def train_train_cmd(language, font, shell_type, outdir=os.path.curdir):
    train_m.create_tesseract_trainFile(language, font, shell_type, outdir)

#
def train_get_raw(url, num, outdir=os.path.curdir):

    train_m.get_raw_captcha(url, num, outdir=outdir)
    #print(url, num, outdir)


def main_preprocessing(path, preprocessing_method, outdir=os.path.curdir):

    imgObj, image_path = get_image(path)

    # from list to set

    assert preprocessing_method in preprocessing_method_dict.keys(), 'invalid params in -prepro'

    imgObj = preprocessing_method_dict[preprocessing_method](imgObj)
    #imgObj.show()

    newpath = add_postfix(image_path, PREPROCESSING_FLAG_DICT[preprocessing_method])
    imgObj.save(newpath)



def main_split(path, num=None, split_method='bisect', outdir=os.path.curdir):
    #path, n=None, split_method='bisect', outdir=os.path.curdir

    assert split_method in split_method_dict, 'split_method do not exist!'

    assert num!=None or split_method != 'bisect','bisect method need the param n'
    split_method = split_method_dict[split_method]

    imgObj, image_path = get_image(path)
    box_img = split_method(imgObj, n=num)


    # base_path = os.path.join(outdir, os.path.basename(path))
    for i, sub_img in enumerate(box_img):

        sub_img_path = add_postfix(image_path, '{0:d}'.format(i))
        sub_img.save(sub_img_path)



def recognise_tesseract(path, args=None):

    try:
        result = rg.tesseract(path, args)
    except Exception as ex:
        color.print_err(ex)
    else:
        color.print_info(result, len(result))




def main(args):
    print(args)
    pass


def interactive():
    parser_main = ArgumentParser()
    sub_parsers = parser_main.add_subparsers(help='main-sub-command')


    # main_parser

################################################################################
    # sub_parser: preprocessing
    parser_preprocessing = sub_parsers.add_parser('preproc',
                                                  help='preprocessing the image')

    parser_preprocessing.add_argument('path', nargs='?',
                                      help='image file path(exclude image url)')

    parser_preprocessing.add_argument('-o', '--outdir', help='output directory default curdir')
    parser_preprocessing.add_argument('-m', '--method',
                                      dest='preprocessing_method',
                                      nargs = '?',
                                      required = True,
                                      choices=['binary', 'clear_noise', 'sharpen', 'remove_frame'],
                                      help='preprocessing method')

    parser_preprocessing.set_defaults(func=main_preprocessing)

################################################################################
    # sub_parser: train
    parser_train = sub_parsers.add_parser('train', help='train the captcha data')
    train_sub_parsers = parser_train.add_subparsers(help='train-sub-command')
    # train_sub_parser: get_raw
    parser_train_getRawCaptcha = train_sub_parsers.add_parser('get_raw',
                                                              help='get the raw captcha data')

    parser_train_getRawCaptcha.add_argument('url', nargs='?',
                                            help='raw captcha url')

    parser_train_getRawCaptcha.add_argument('-n', '--num', type=int,
                                            help='the number of raw captcha')

    parser_train_getRawCaptcha.add_argument('-o', '--outdir', help='output directory default curdir')

    parser_train_getRawCaptcha.set_defaults(func=train_get_raw)

    ## train_sub_parser: train_cmd
    parser_train_trainCmd = train_sub_parsers.add_parser('train_cmd',
                                                         help='create train cmd file')

    parser_train_trainCmd.add_argument('-l', '--language', help='language')
    parser_train_trainCmd.add_argument('-font', '--font', help='font name')
    parser_train_trainCmd.add_argument('-o', '--outdir', help='output directory default curdir')
    parser_train_trainCmd.add_argument('-shell', '--shell', dest='shell_type',
                                       choices=['cmd', 'bash'], help='cmd shell type')

    parser_train_trainCmd.set_defaults(func=train_train_cmd)
################################################################################
    # sub_parser: split
    parser_split = sub_parsers.add_parser('split', help='split the image')
    parser_split.add_argument('path', nargs='?',
                              help='image file path(exclude image url)')

    parser_split.add_argument('-n', '--num', type=int,
                              help='point the number of char of img')

    parser_split.add_argument('-m', '--method', dest='split_method',
                              choices=['bisect', 'boxsplit'],
                              help='split method (default bisect)')

    parser_split.add_argument('-o', '--outdir', help='output directory default curdir')
    parser_split.set_defaults(func=main_split)

################################################################################

    # sub_parser: recognise
    parser_recognise = sub_parsers.add_parser('recognise',
                                              help='recognise the captcha')

    recognise_sub_parsers = parser_recognise.add_subparsers(help='recognise-sub-command')

    ## recognise_sub_parser: tesseract
    parser_recognise_tesseract = recognise_sub_parsers.add_parser('tesseract',
                                                                  help='recognise the captcha using tesseract')
    parser_recognise_tesseract.add_argument('path', nargs='?', help='image file path(exclude image url)')
    parser_recognise_tesseract.add_argument('-args', type=str, help='equivalent tesseract "args" stdout ')

    parser_recognise_tesseract.set_defaults(func=recognise_tesseract)


################################################################################
    parse_result = parser_main.parse_args()
    args = remove_value(remove_key(parse_result.__dict__, 'func'), None)
    parse_result.func(**args)




if __name__ == '__main__':
    interactive()