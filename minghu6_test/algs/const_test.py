# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""


def test_const():
    from minghu6.algs import const

    const.SUCCESSFUL_UPPER_EXAMPLE = 1
    try:
        const.failed_lower_example = 1
    except const.ConstCaseWarning as ex:
        # print(ex)
        pass


if __name__ == '__main__':
    test_const()
