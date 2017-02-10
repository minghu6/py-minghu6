#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from collections import namedtuple

from minghu6.algs.decorator import singleton
from minghu6.text.seq_enh import INVALID_FILE_CHAR_SET

__all__ = ['EscapeCharsetMap',
           'ESCAPED_CHARSET_MAP_DICT',
           'char_escape',
           'htmltitle2path']


EscapeCharsetMap = namedtuple('EscapeCharsetMap', ['html', 'url'])
@singleton
class EscapeCharsetMapClass:

    def __getitem__(self, char):
        hex_str = '{0:04x}'.format(ord(char))
        base_ten_str = '{0:03d}'.format(ord(char))
        return EscapeCharsetMap(url='%{0:s}'.format(hex_str),
                                html='&#{0:s}'.format(base_ten_str))

ESCAPED_CHARSET_MAP_DICT = EscapeCharsetMapClass()
def char_escape(s:str, escape_charset, escape_char_type:str):
    """
    :param s:
    :param escape_charset: None means all char will be escaped
    :param escape_char_type:
    :return:
    """
    if escape_charset is not None:
        new_s = s
        for each_escape_char in escape_charset:
            new_s=new_s.replace(each_escape_char,
                        getattr(ESCAPED_CHARSET_MAP_DICT[each_escape_char], escape_char_type))
    else:
        new_s = []
        for each_char in s:
            new_s.append(getattr(ESCAPED_CHARSET_MAP_DICT[each_char], escape_char_type))

        new_s = ''.join(new_s)
        s = new_s

    return s

def htmltitle2path(htmltitle, escape_char_type='url'):

    path=char_escape(htmltitle, INVALID_FILE_CHAR_SET, escape_char_type)
    path = ''.join(re.split('\s+', path)) # in case other blank char
    return path