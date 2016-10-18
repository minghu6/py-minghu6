# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
About Decode and Encode about str bytes etc
(To fix bugs when transfer code from Python2 to Python3)
################################################################################
"""
def get_locale_codec():
    """
    Is Very Very Useful
    :return:
    """
    import locale
    import codecs
    return codecs.lookup(locale.getpreferredencoding()).name

def str2bytes(origin_str,charset='utf-8'):
    """

    :param origin_str:
    :param charset:
    :return:immutable struct
    """
    return bytearray(origin_str,encoding=charset)

def bytes2str(origin_bytes,charset='utf-8'):

    return origin_bytes.decode(encoding=charset,errors='ignore')

def get_decode_html(openurl_obj,default_charset='utf-8'):
    """
    Python3 urlopen return str but bytes
    :param request: request=urllib.request.Request(url,None,headers)
    :return:
    """
    html=openurl_obj.read()
    codec = openurl_obj.info().get_param('charset', default_charset)
    html = html.decode(codec,errors='ignore')

    return html

if __name__ == '__main__':

    s1=str2bytes('123')
    b2=bytes2str(s1)
    print(s1,type(s1))
    print(b2,type(b2))

    print(get_locale_codec())