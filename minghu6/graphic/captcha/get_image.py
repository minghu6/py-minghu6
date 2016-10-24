# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
from a URI open the captcha Image Pillow PIL.Image
"""
from PIL import Image
import os
class NotValidPathStr(BaseException):pass

def get_image(s:str, outdir=None):

    from urllib.request import urlretrieve


    import re
    from minghu6.text.pattern import url_net
    pattern_url_net = url_net
    if re.match(pattern_url_net, s) != None:
        if outdir != None:
            filepath = os.path.join(outdir, 'captcha')
        else:
            filepath = 'captcha'
        urlretrieve(s, filename='captcha')
        imgObj = Image.open(filepath)
        #imgObj.show()
        return imgObj, filepath
    elif os.path.isfile(s):
        imgObj = Image.open(s)
        return imgObj, s
    else:
        raise NotValidPathStr(s)


if __name__ == '__main__':
    img=get_image(r'http://zyzfw.xidian.edu.cn/site/captcha')
    img.show()