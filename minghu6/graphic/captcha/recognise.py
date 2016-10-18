# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
recognise the captcha
"""
#import subprocess
from minghu6.etc.cmd import exec_cmd
from minghu6.etc.cmd import has_proper_tesseract
from minghu6.etc.cmd import DoNotHaveProperVersion

def tesseract(path):
    if not has_proper_tesseract():
        raise DoNotHaveProperVersion

    cmd_str = 'tesseract -psm 8 {0} stdout digits'.format(path)
    info_lines, err_lines = exec_cmd(cmd_str)

    try:
        captchaResponse = info_lines[0].strip()
    except IndexError:
        raise Exception(''.join(err_lines))
    else:
        return captchaResponse