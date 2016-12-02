# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from urllib.request import urlopen, Request, urljoin
from bs4 import BeautifulSoup
import requests
import re
from minghu6.http.request import headers, headers_mobile

def zyzfw_xidian_edn_cn(cookies:[dict, requests.cookies.RequestsCookieJar]=None,
                        session=None):

    url="http://zyzfw.xidian.edu.cn/"
    if session == None:
        session = requests.Session()

    if cookies != None:
        session.cookies.update(cookies)
    r=session.request(url=url,headers=headers,method='get')
    bsObj=BeautifulSoup(r.text, 'html.parser')
    links = []
    for link in bsObj.find('div', {'class' : 'container'}).find('div', {'class' : 'site-login'}).find('div', {'class' : 'col-lg-4'}):
        links.append(link)

    target_s=str(links[0])
    pattern_src=r'(?<=src=").*(?="/>)'
    result=re.search(pattern_src, target_s)

    url_captcha=urljoin(url, result.group(0))



    links = []
    for link in bsObj.find('form', {'id' : 'login-form'}):
        links.append(link)
    target_s=str(links[1])
    pattern_src=r'(?<=name="_csrf" type="hidden" value=").*(?="> )'
    result=re.search(pattern_src, target_s)
    _csrf=result.group(0)


    return url_captcha, session, _csrf

def pythonscraping_com_humans_only(cookies:[dict, requests.cookies.RequestsCookieJar]=None,
                                   session=None):

    if session == None:
        session = requests.Session()

    html = session.get("http://www.pythonscraping.com/humans-only").text
    bsObj = BeautifulSoup(html, "html.parser")
    #Gather prepopulated form values
    imageLocation = bsObj.find("img", {"title": "Image CAPTCHA"})["src"]
    formBuildId = bsObj.find("input", {"name":"form_build_id"})["value"]
    captchaSid = bsObj.find("input", {"name":"captcha_sid"})["value"]
    captchaToken = bsObj.find("input", {"name":"captcha_token"})["value"]

    captchaUrl = "http://pythonscraping.com"+imageLocation

    return captchaUrl, session




url_captcha_dict = {'http://zyzfw.xidian.edu.cn/':zyzfw_xidian_edn_cn,
                    'http://www.pythonscraping.com/humans-only':pythonscraping_com_humans_only}
