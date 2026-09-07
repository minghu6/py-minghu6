# -*- coding:utf-8 -*-

import minghu6.functools as functools


def test_chain_apply():
    import operator
    from functools import partial

    funcs = [partial(operator.add, 1), partial(operator.mul, 2)]
    assert functools.compose(*funcs, 3) == 7


if __name__ == "__main__":
    test_chain_apply()
