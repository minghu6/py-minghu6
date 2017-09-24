# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
A captcha deal tools
"""
import asyncio
import os
import re
import sys
import uuid
from argparse import ArgumentParser
from subprocess import Popen, PIPE

import minghu6.graphic.captcha.train as train_m
from minghu6.algs.asyn import AsyncIteratorWrapper
from minghu6.algs.userdict import remove_key, remove_value
from minghu6.etc.importer import check_module
from minghu6.etc.path import add_postfix
from minghu6.graphic.captcha import preprocessing as pp
from minghu6.graphic.captcha import recognise as rg
from minghu6.graphic.captcha.get_image import get_image
from minghu6.http.request import headers
from color import color
from minghu6.text.pattern import ext as pattern_ext

check_module('aiohttp')  # aiohttp are not in requirements because of less use
import async_timeout
import aiohttp

preprocessing_method_dict = {'binary': pp.binary_img,
                             'clear_noise': pp.clearNoise_img,
                             'sharpen': pp.sharpen_img,
                             'remove_frame': pp.removeFrame_img}

split_method_dict = {'bisect': pp.bisect_img,
                     'boxsplit': pp.boxsplit_img}

recognise_method_dict = {'tesseract': rg.tesseract}

PREPROCESSING_FLAG_DICT = {'binary': 'b',
                           'clear_noise': 'cln',
                           'sharpen': 'shp',
                           'remove_frame': 'rf'}  # output image name postfix


def train_train_cmd(language, font, shell_type, outdir=os.path.curdir):
    train_m.create_tesseract_trainFile(language, font, shell_type, outdir)


#
def train_get_raw(url, num, outdir=os.path.curdir):
    train_m.get_raw_captcha(url, num, outdir=outdir)
    # print(url, num, outdir)


def main_preprocessing(path, preprocessing_method, outdir=os.path.curdir, width=None):
    imgObj, image_path = get_image(path)

    # from list to set

    assert preprocessing_method in preprocessing_method_dict.keys(), 'invalid params in -prepro'
    other_kwargs = {}
    if preprocessing_method == 'remove_frame' and width is not None:
        other_kwargs['frame_width'] = int(width)

    try:
        imgObj = preprocessing_method_dict[preprocessing_method](imgObj, **other_kwargs)
        # imgObj.show()
    except pp.ImageSizeError as ex:
        print(ex)

    newpath = add_postfix(image_path, PREPROCESSING_FLAG_DICT[preprocessing_method])
    imgObj.save(newpath)


def main_split(path, num=None, split_method='bisect', outdir=os.path.curdir):
    # path, n=None, split_method='bisect', outdir=os.path.curdir

    assert split_method in split_method_dict, 'split_method do not exist!'

    assert num is not None or split_method != 'bisect', 'bisect method need the param n'
    split_method = split_method_dict[split_method]

    imgObj, image_path = get_image(path)
    box_img = split_method(imgObj, n=num)

    # base_path = os.path.join(outdir, os.path.basename(path))
    for i, sub_img in enumerate(box_img):
        sub_img_path = add_postfix(image_path, '{0:d}'.format(i))
        sub_img.save(sub_img_path)


def main_fetch(url, num, outdir, captcha_pattern, ext=None):
    kwargs = locals()  # collect all kwargs of func main_fetch
    if ext is not None and re.match(pattern_ext, ext) is None:
        color.print_err('error -ext arg, should be .png, .jpg ect.')
        return

    pyfile_path = os.path.join(os.path.dirname(__file__), 'convert_image_p.py')
    p = Popen([sys.executable, pyfile_path, str(num), ext],
              stdin=PIPE, stderr=sys.stderr, stdout=sys.stdout,
              bufsize=1000)
    p.stdin.encoding = 'utf8'

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(_main_fetch(loop, p, url, **kwargs))
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    p.kill()


async def _main_fetch(loop, p, url, num, outdir, captcha_pattern, ext=None):
    async def fetch(session, url):
        with async_timeout.timeout(5):
            async with session.get(url) as response:
                return await response.read()

    session = aiohttp.ClientSession(loop=loop, headers=headers)
    async for i in AsyncIteratorWrapper(range(num)):
        captcha_name = captcha_pattern.replace('$(NO)', str(i)).replace('$(UUID)', str(uuid.uuid4()))
        path = os.path.join(outdir, captcha_name)
        while True:
            try:
                content = await fetch(session, url)
            except asyncio.TimeoutError as ex:
                color.print_err(ex)
            else:
                break

        with open(path, 'wb') as fw:
            fw.write(content)

        print('download %s' % path)
        p.stdin.write(path.encode() + b'\n')

    p.stdin.flush()


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


def cli():
    parser_main = ArgumentParser(prog='captcha', description='A captcha processor')
    parser_main.set_defaults(func=parser_main.print_usage)
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
                                      nargs='?',
                                      required=True,
                                      choices=['binary', 'clear_noise', 'sharpen', 'remove_frame'],
                                      help='preprocessing method')
    parser_preprocessing.add_argument('-w', '--width',
                                      required=False,
                                      help='frame width to remove(default 2 pix)')

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

    # sub_parser: fetch
    parser_fetch = sub_parsers.add_parser('fetch',
                                          help='fetch captcha batch')

    parser_fetch.add_argument('url', help='captcha url')

    parser_fetch.add_argument('-n', '--num', type=int, required=True,
                              help='fetch number')

    parser_fetch.add_argument('-o', '--outdir', default=os.curdir,
                              help='captcha store path')

    parser_fetch.add_argument('-ext', '--ext', help='captcha ext, such as .png')
    parser_fetch.add_argument('-p', '--pattern', dest='captcha_pattern',
                              default='$(UUID)',
                              help=('captcha name pattern, support macro UUID and NO\n'
                                    'such as $(UUID)_download, '
                                    'download_$(UUID), '
                                    '$(UUID)_$(NO) etc.'))

    parser_fetch.set_defaults(func=main_fetch)

    ################################################################################
    parse_result = parser_main.parse_args()
    # remove_key(parse_result.__dict__, 'func'),
    args = remove_value(remove_key(parse_result.__dict__, 'func'), None)
    parse_result.func(**args)


if __name__ == '__main__':
    cli()
