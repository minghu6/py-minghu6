# -*- coding:utf-8 -*-

from copy import deepcopy

from minghu6.operators import *
from minghu6.test import assert_exception


def test_getone():
    assert get(["a", "b", "c"], 2) == "c"
    assert get(["a", "b"], 2, default="c") == "c"
    ran = range(10)
    ran_copy = deepcopy(ran)
    assert get(ran, 2) == 2
    assert ran == ran_copy
    assert get({"a": 1, "b": 2}, "b") == 2


@assert_exception(IndexError)
def test_getone_with_exception_index():
    get(range(5), 5)


@assert_exception(KeyError)
def test_getone_with_exception_key():
    get({}, "key")

