# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import requests
from bs4 import BeautifulSoup

from minghu6.graphic.captcha.url_captcha import CAPTCHA_ID

class KwargsError(BaseException):

    def __str__(self):
        return 'error args'


def pythonscraping__com_humans_only(session=None, **kwargs):

    if session == None:
        session = requests.session()

    try:
        captchaToken = kwargs['captcha_token']
        captchaSid = kwargs['captcha_sid']
        captchaResponse = kwargs[CAPTCHA_ID]
        formBuildId = kwargs['form_build_id']
    except KeyError:
        raise KwargsError


    params = {
        "captcha_token":captchaToken, "captcha_sid":captchaSid,
        "form_id":"comment_node_page_form", "form_build_id": formBuildId,
        "captcha_response":captchaResponse, "name":"一个模拟登陆的人",
        "subject": "到此一游",
        "comment_body[und][0][value]":
        "我不是个机器人"
    }

    r = session.post("http://www.pythonscraping.com/comment/reply/10",
                      data=params)
    responseObj = BeautifulSoup(r.text, 'html.parser')
    if responseObj.find("div", {"class":"messages"}) is not None:
        print(responseObj.find("div", {"class":"messages"}).get_text())

    return r.text


def zyzfw_xidian_edn_cn(session=None, **kwargs):

    if session == None:
        session = requests.session()

    try:
        _csrf = kwargs['_csrf']
        captcha = kwargs[CAPTCHA_ID]
    except KeyError:
        raise KwargsError

    params = {
        "_csrf":_csrf, "LoginForm[verifyCode]":captcha,
        "LoginForm[username]":"13030211023", "LoginForm[password]": '19678zy',
        "login-button":""
    }
    r = session.post("http://zfw.xidian.edu.cn/",
                      data=params)

    return r.text


url_logon_dict = {'http://www.pythonscraping.com/humans-only':pythonscraping__com_humans_only,
                  'http://zfw.xidian.edu.cn/':zyzfw_xidian_edn_cn,}



if __name__ == '__main__':
    raise KwargsError