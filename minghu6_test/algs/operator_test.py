# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from copy import deepcopy

from minghu6.algs import operator as op
from minghu6.algs.decorator import assert_exception


def test_getitem():
    assert op.getitem(['a', 'b', 'c'], 2) == 'c'
    assert op.getitem(['a', 'b'], 2, 'c') == 'c'
    ran = range(10)
    ran_copy = deepcopy(ran)
    assert op.getitem(ran, 2) == 2
    assert ran == ran_copy
    assert op.getitem({'a':1, 'b':2}, 'b') == 2


@assert_exception(IndexError)
def test_getitem_with_exception_index():
    op.getitem(range(5), 5)


@assert_exception(KeyError)
def test_getitem_with_exception_key():
    op.getitem({}, 'key')


def test_c_not():
    op.c_not(1) == 1
    op.c_not(2) == 1
    op.c_not(0) == 0
    op.c_not(None) == 0
    op.c_not([]) == 1


if __name__ == '__main__':
    test_getitem()
    test_c_not()
    test_getitem_with_exception_index()
    test_getitem_with_exception_key()
