# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
from a URI open the captcha Image Pillow PIL.Image
"""
from PIL import Image
import requests

import os
class NotValidPathStr(BaseException):pass

def get_image(s:str, outdir=None, session:requests.Session=None):

    from urllib.request import urlretrieve


    import re
    from minghu6.text.pattern import url_net
    pattern_url_net = url_net
    if re.match(pattern_url_net, s) != None:
        if outdir != None:
            filepath = os.path.join(outdir, 'captcha')
        else:
            filepath = 'captcha'

        if session == None:
            if os.path.exists('captcha'):
                os.remove('captcha')
            urlretrieve(s, filename='captcha')
        else:
            r=session.get(s)
            with open('captcha', 'wb') as imgFile:
                imgFile.write(r.content)

        with Image.open(filepath) as imgObj:
            newfilepath = filepath + '.'+imgObj.format.lower()

        if os.path.exists(newfilepath):
            os.remove(newfilepath)

        os.rename(filepath, newfilepath)
        imgObj = Image.open(newfilepath)

        #imgObj.show()
        return imgObj, newfilepath
    elif os.path.isfile(s):
        imgObj = Image.open(s)
        return imgObj, s
    else:
        raise NotValidPathStr(s)

