# -*- coding:utf-8 -*-

from minghu6.etc.pprint import *

def test_format_int():
    result = format_int(10000000000, seg=3, delimiter="_")
    assert result == "10_000_000_000"


if __name__ == "__main__":
    test_format_int()
