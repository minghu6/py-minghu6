# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
recognise the captcha
"""
import requests
from minghu6.etc.cmd import DoNotHaveProperVersion
# import subprocess
from minghu6.etc.cmd import exec_cmd
from minghu6.etc.cmd import has_proper_tesseract
from minghu6.graphic.captcha.get_image import get_image

__all__ = ['tesseract']


def tesseract(path, limit_config=None, args=None, session: requests = None):
    if not has_proper_tesseract():
        raise DoNotHaveProperVersion

    imgObj, image_path = get_image(path, session=session)

    if args is None:
        cmd_str = 'tesseract -psm 8 {0} stdout '.format(image_path)
    else:
        cmd_str = ' '.join(['tesseract', args, image_path, 'stdout'])
        print(cmd_str)

    if limit_config is not None:  # like digits
        cmd_str += ' {0}'.format(limit_config)

    info_lines, err_lines = exec_cmd(cmd_str, shell=True)

    try:
        captchaResponse = info_lines[0].strip()
    except IndexError:
        raise Exception(''.join(err_lines))
    else:
        return captchaResponse
