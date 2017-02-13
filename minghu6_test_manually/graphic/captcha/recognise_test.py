# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.algs.decorator import skip

@skip
def tesseract_test():
    from minghu6.graphic.captcha.recognise import tesseract

    result= tesseract('http://zyzfw.xidian.edu.cn/site/captcha')
    print(result)

if __name__ == '__main__':
    #tesseract_test()
    pass