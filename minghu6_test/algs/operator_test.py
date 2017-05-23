# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from functools import reduce, partial

from minghu6.algs import operator as op


def test_getitem():
    assert op.getitem(['a', 'b', 'c'], 2) == 'c'
    assert op.getitem(['a', 'b'], 2, 'c') == 'c'
    assert op.getitem(['a', 'b'], 2) is None


def test_add_pow():
    assert reduce(op.add,
                  map(partial(op.pow, y=2), [1, 2, 3])) == 14


def test_c_not():
    bool(op.c_not(1)) == False
    bool(op.c_not(2)) == False
    bool(op.c_not(0)) == True


if __name__ == '__main__':
    test_getitem()
    test_add_pow()
    test_c_not()
