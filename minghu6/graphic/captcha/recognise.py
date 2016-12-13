# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
recognise the captcha
"""
#import subprocess
from minghu6.etc.cmd import exec_cmd
from minghu6.etc.cmd import has_proper_tesseract
from minghu6.etc.cmd import DoNotHaveProperVersion
from minghu6.graphic.captcha.get_image import get_image

from PIL import Image
import requests
import os
def tesseract(path, args=None, session:requests=None):
    if not has_proper_tesseract():
        raise DoNotHaveProperVersion

    imgObj, image_path=get_image(path, session=session)

    if args == None:
        cmd_str = 'tesseract -psm 8 {0} stdout '.format(image_path)
    else:
        cmd_str = ' '.join(['tesseract', args, 'stdout'])

    info_lines, err_lines = exec_cmd(cmd_str)

    try:
        captchaResponse = info_lines[0].strip()
    except IndexError:
        raise Exception(''.join(err_lines))
    else:
        return captchaResponse