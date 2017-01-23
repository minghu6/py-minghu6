# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.algs import var

def test_allis():
    from minghu6.algs.var import allis
    assert allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

def test_allequal():
    assert var.allequal([11, 12, 13], (11, 12, 13)) == True
    assert var.allequal([11, 12, 13], [11, 12, 14]) == False

def test_isnum_str():
    from minghu6.algs.var import isnum_str

    assert isnum_str('1023') == True

    assert isnum_str('1ab2') == False




if __name__ == '__main__':

    test_allis()
    test_allequal()
    test_isnum_str()
