#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from collections import namedtuple

from minghu6.algs.decorator import singleton
from minghu6.text.seq_enh import INVALID_FILE_CHAR_SET

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
    for each_escape_char in escape_charset:
        s=s.replace(each_escape_char,
                    getattr(ESCAPED_CHARSET_MAP_DICT[each_escape_char], escape_char_type))

    return s

def htmltitle2path(htmltitle, escape_char_type='url'):

    path=char_escape(htmltitle, INVALID_FILE_CHAR_SET, escape_char_type)
    path = ''.join(re.split('\s+', path)) # in case other blank char
    return path