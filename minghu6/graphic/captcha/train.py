# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

import os

from minghu6.etc.path import add_postfix
from minghu6.graphic.captcha.get_image import get_image

__all__ = ['get_raw_captcha',
           'create_tesseract_trainFile']


def get_raw_captcha(url, n, outdir=os.curdir, session=None):
    for i in range(n):
        captcha_name = add_postfix('captcha', str(i))
        get_image(url, captcha_name=captcha_name, outdir=outdir)


def create_tesseract_trainFile(language, font, shell_type, outdir=os.curdir):
    """
    shell type cmd | bash
    :param shell_type:
    :return:
    """
    common_shellStr1 = ['# create box file',
                        'tesseract '
                        '-psm 8 '
                        '{l}.{font}.exp0.tif '
                        '{l}.{font}.exp0 '
                        '-l eng batch.nochop makebox',

                        'tesseract '
                        '-psm 8 '
                        '{l}.{font}.exp0.tif '
                        '{l}.{font}.exp0 nobatch box.train',

                        'unicharset_extractor {l}.{font}.exp0.box',

                        'echo "{font} 0 0 0 0 0" > font_properties',

                        'shapeclustering '
                        '-F font_properties '
                        '-U unicharset {l}.{font}.exp0.tr',

                        'mftraining '
                        '-F font_properties '
                        '-U unicharset '
                        '-O {l}.unicharset {l}.{font}.exp0.tr',

                        'cntraining {l}.{font}.exp0.tr']

    bash_str = ['mv inttemp {l}.inttemp',
                'mv normproto {l}.normproto',
                'mv pffmtable {l}.pffmtable',
                'mv shapetable {l}.shapetable']

    cmd_str = ['rename inttemp {l}.inttemp',
               'rename normproto {l}.normproto',
               'rename pffmtable {l}.pffmtable',
               'rename shapetable {l}.shapetable']

    common_shellStr2 = ['combine_tessdata {l}.']

    shell_str = []
    if shell_type == 'cmd':
        shell_str = common_shellStr1 + cmd_str + common_shellStr2

    elif shell_type == 'bash':
        shell_str = common_shellStr1 + bash_str + common_shellStr2

    else:
        raise Exception('shell type is error')

    shell_str = '\n'.join(shell_str).format(l=language, font=font)

    with open('train_{0}_{1}_{2}.txt'.format(shell_type,
                                             language,
                                             font), 'w') as file:

        file.write(shell_str)
