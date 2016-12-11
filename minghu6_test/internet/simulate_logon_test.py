# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def pythonscraping__com_humans_only_test():
    from minghu6.internet.simulate_logon import pythonscraping__com_humans_only as logon
    from minghu6.graphic.captcha.url_captcha import pythonscraping__com_humans_only as get
    from minghu6.graphic.captcha.get_image import get_image

    responseSet = get()

    captchaUrl, session = responseSet[:2]
    params_dict = responseSet[-1]

    imgObj , _ = get_image(captchaUrl)
    imgObj.show()
    captcha = input('input captcha please\n').strip()
    params_dict['captcha_response'] = captcha
    logon(session=session, **params_dict)
    print(params_dict)



if __name__ == '__main__':

    pythonscraping__com_humans_only_test()