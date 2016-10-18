# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
recognise the captcha
"""
import subprocess
from minghu6.etc.cmd import has_proper_tesseract
from minghu6.etc.cmd import DoNotHaveProperVersion

def tesseract(path):
    if not has_proper_tesseract():
        raise DoNotHaveProperVersion

    p = subprocess.Popen(["tesseract", path, "captcha"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    f = open("captcha.txt", "r")
    #Clean any whitespace characters
    captchaResponse = f.read().replace(" ", "").replace("\n", "")
    return captchaResponse