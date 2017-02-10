# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.algs import operator
def test_getitem():
    assert operator.getitem(['a', 'b', 'c'], 2) == 'c'
    assert operator.getitem(['a', 'b'], 2, 'c') == 'c'
    assert operator.getitem(['a', 'b'], 2) is None

if __name__ == '__main__':
    test_getitem()