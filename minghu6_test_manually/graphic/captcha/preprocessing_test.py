# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import os

from PIL import Image
from minghu6.algs.decorator import skip
from minghu6.etc.path import get_cwd_preDir
from minghu6.graphic.captcha import preprocessing as preproc


@skip
def clearNoise_img_test():
    gif_file_path = os.path.join(get_cwd_preDir(3),
                                 'resources',
                                 'minghu6_test',
                                 'etc',
                                 'captcha.gif')

    with Image.open(gif_file_path) as imgObj:
        imgObj = preproc.clearNoise_img(imgObj)
        imgObj.show()


if __name__ == '__main__':
    # clearNoise_img_test()
    pass
