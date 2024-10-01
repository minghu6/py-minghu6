# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from minghu6.meta import var


def test_istypeof():
    assert var.istypeof(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))


def test_isnum_str():
    assert var.isnumstr('1023') == True

    assert var.isnumstr('1ab2') == False


def test_isiterable():
    assert not var.isiterable('abc')
    assert not var.isiterable(b'abc')
    assert not var.isiterable(bytearray(b'abc'))
    assert var.isiterable('abc', but_str_bytes=False)

    assert var.isiterable(['a', 'b', 'c'])
    assert var.isiterable(('a', 'b', 'c'))



if __name__ == '__main__':
    test_istypeof()
    test_isnum_str()
    test_isiterable()
