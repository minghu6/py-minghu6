# -*- coding:utf-8 -*-

import minghu6.functools as functools


def test_chain_apply():
    import operator
    from functools import partial
    funcs = [partial(operator.add, 1), partial(operator.mul, 2)]
    assert functools.chain_apply(funcs, 3) == 8


def test_flatten():
    assert list(functools.flatten([[1, 2], 3, [4], [5, [1, [2]]]])) == [1, 2, 3, 4, 5, 1, 2]


if __name__ == '__main__':
    test_chain_apply()
    test_flatten()
