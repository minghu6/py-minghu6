# -*- Coding:utf-8 -*-
"""

"""
import doctest


def test_lower_bound():
    from minghu6.algs.stl import lower_bound
    doctest.run_docstring_examples(lower_bound, locals())

    assert lower_bound([1, 2, 3, 4], 3) == 2


def test_upper_bound():
    from minghu6.algs.stl import upper_bound
    doctest.run_docstring_examples(upper_bound, locals())


if __name__ == '__main__':
    test_lower_bound()
    test_upper_bound()
