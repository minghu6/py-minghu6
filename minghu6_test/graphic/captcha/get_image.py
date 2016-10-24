# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def get_image_test():
    from minghu6.graphic.captcha.get_image import get_image
    imgObj = get_image('http://zyzfw.xidian.edu.cn/site/captcha')
    imgObj.show()
    imgObj.save('captcha_tesseract', 'png')

if __name__ == '__main__':

    get_image_test()
