# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import requests

def get_image_test():
    from minghu6.graphic.captcha.get_image import get_image
    session = requests.Session()

    imgObj = get_image('http://zyzfw.xidian.edu.cn/site/captcha?v=5832eb2835057', session=session)[0]
    imgObj.show()

    imgObj = get_image('http://zyzfw.xidian.edu.cn/site/captcha?v=5832eb2835057', session=session)[0]
    imgObj.show()


if __name__ == '__main__':

    get_image_test()
