# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from functools import reduce, partial
from minghu6.algs import operator
def test_getitem():
    assert operator.getitem(['a', 'b', 'c'], 2) == 'c'
    assert operator.getitem(['a', 'b'], 2, 'c') == 'c'
    assert operator.getitem(['a', 'b'], 2) is None

def test_add_pow():
    assert reduce(operator.add,
                  map(partial(operator.pow, y=2), [1, 2, 3])) == 14

if __name__ == '__main__':
    test_getitem()
    test_add_pow()