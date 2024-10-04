

import minghu6.itertools
from minghu6.itertools import *
from minghu6.test.doctest import run_doctest



def test_iterator_zip_eq():
    def gen1():
        yield from [11, 12, 13]

    assert zip_eq([11, 12, 13], iter((11, 12, 13)), gen1())
    assert zip_eq([11, 12, 13], [11, 12, 14]) == False


def test_flatten():
    assert list(flattenall([[1, 2], 3, [4], [5, [1, [2]]]])) == [
        1,
        2,
        3,
        4,
        5,
        1,
        2,
    ]


if __name__ == "__main__":
    test_iterator_zip_eq()
    run_doctest(minghu6.itertools)
