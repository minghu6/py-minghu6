
from minghu6.itertools import *


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
