# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from minghu6.string import *


def test_split_whitespace():
    s1 = "a  bb ccc   dddd"
    assert split_whitespace(s1) == ["a", "bb", "ccc", "dddd"]


def test_split_blankline():
    s1 = """abc
def

ghi

"""
    target1 = ["abc\ndef", "ghi"]
    assert split_blankline(s1) == target1


def test_camelize():
    name1 = camelize("a_class_b_d")
    assert name1 == "AClassBD", name1

    name2 = camelize("a_class_bd")
    assert name2 == "AClassBd", name2

    name3 = camelize("a_class_b_d", upper_camel_case=False)
    assert name3 == "aClassBD", name3

    name4 = camelize("a-class-b-d")
    assert name4 == "AClassBD", name4


def test_underscore():
    name1 = underscore("IOError")
    assert name1 == "io_error", name1

    name2 = underscore("AClassBD", strict=True)
    assert name2 == "a_class_b_d", name2

    name3 = underscore("IOError", strict=True)
    assert name3 == "i_o_error", name3

    name4 = underscore("abc_def")
    assert name4 == "abc_def", name4


if __name__ == "__main__":
    test_split_whitespace()
    test_split_blankline()
    test_camelize()
    test_underscore()
