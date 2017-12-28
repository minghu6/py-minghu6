# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from minghu6.algs import var


def test_allis():
    assert var.allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))


def test_each_same():
    def gen1():
        yield from [11, 12, 13]

    assert var.each_same([11, 12, 13], (11, 12, 13), gen1())
    assert var.each_same([11, 12, 13], [11, 12, 14]) == False
    assert var.each_same([11, 11, 11])
    assert var.each_same([])
    assert var.each_same([1])
    assert not var.each_same([11, 12, 11])

    from collections import namedtuple
    SomeOneTuple = namedtuple('SomeOneTuple', ['x', 'y'])
    assert not var.each_same([SomeOneTuple(1, 2), SomeOneTuple(1, 1)],
                             key=lambda x: (x.x, x.y))


def test_isnum_str():
    assert var.isnum_str('1023') == True

    assert var.isnum_str('1ab2') == False


def test_isiterable():
    assert not var.isiterable('abc')
    assert not var.isiterable(b'abc')
    assert not var.isiterable(bytearray(b'abc'))
    assert var.isiterable('abc', but_str_bytes=False)

    assert var.isiterable(['a', 'b', 'c'])
    assert var.isiterable(('a', 'b', 'c'))


def test_custom_str():
    cs = var.CustomStr('aaa ')
    cs2 = cs.strip()
    assert cs2 == var.CustomStr('aaa')
    cs2.extra_attrs['status'] = 'Y'
    
    assert isinstance(cs2, var.CustomStr)
    assert cs2 != var.CustomStr('aaa')
    assert cs2.extra_attrs['status'] == 'Y'


def test_custom_bytes():
    cb = var.CustomBytes(b'aaa ')
    cbytes2 = cb.strip()
    assert cbytes2 == var.CustomBytes(b'aaa')
    cbytes2.extra_attrs['status'] = 'Y'
    
    assert isinstance(cbytes2, var.CustomBytes)
    assert cbytes2 != var.CustomBytes(b'aaa')
    assert cbytes2.extra_attrs['status'] == 'Y'


def test_custom_bytes_str():
    cs = var.CustomStr('aaa')
    cb = cs.encode()
    assert isinstance(cb, var.CustomBytes)
    assert isinstance(cb, bytes)
    assert not isinstance(cb, str)

    cs.extra_attrs['status'] = 'Yes'
    assert cs.encode().extra_attrs['status'] == 'Yes'

    cb2 = var.CustomBytes(b'bb')
    cb2.extra_attrs['status'] = 'N'
    cs2 = cb2.decode()
    assert isinstance(cs2, str)
    assert isinstance(cs2, var.CustomStr)
    assert cs2.extra_attrs['status'] == 'N', cs2.extra_attrs


if __name__ == '__main__':
    test_allis()
    test_each_same()
    test_isnum_str()
    test_isiterable()
    test_custom_str()
    test_custom_bytes()
    test_custom_bytes_str()
