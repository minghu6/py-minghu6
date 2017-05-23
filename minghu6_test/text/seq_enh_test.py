# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from minghu6.text import seq_enh


def test_split_whitespace():
    s1 = 'a  bb ccc   dddd'
    assert seq_enh.split_whitespace(s1) == ['a', 'bb', 'ccc', 'dddd']


def test_split_blankline():
    s1 = """abc
def

ghi

"""
    target1 = ['abc\ndef', 'ghi']
    assert seq_enh.split_blankline(s1) == target1


if __name__ == '__main__':
    test_split_whitespace()
    test_split_blankline()
