# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.algs import var

def test_allis():
    from minghu6.algs.var import allis
    assert allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

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
                             key=lambda x:(x.x, x.y))

def test_isnum_str():
    from minghu6.algs.var import isnum_str

    assert isnum_str('1023') == True

    assert isnum_str('1ab2') == False

def test_isiterable():
    from minghu6.algs.var import isiterable

    assert not isiterable('abc')
    assert not isiterable(b'abc')
    assert not isiterable(bytearray(b'abc'))
    assert isiterable('abc', but_str_bytes=False)

    assert isiterable(['a', 'b', 'c'])
    assert isiterable(('a', 'b', 'c'))


if __name__ == '__main__':

    test_allis()
    test_each_same()
    test_isnum_str()
    test_isiterable()
