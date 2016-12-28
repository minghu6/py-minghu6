# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

from minghu6.algs import count

def Peak_test():

    l1 = [0, 0, 1, 3, 5, 2, 2, 1, 3, 6, 9, 5, 2]
    p1 = count.Peak(l1)
    res_high=p1.get_peak(count.Peak.HIGH, count.Peak.SORTED_RELATIVE_DISTANCE)

    assert res_high[0].index == 4
    assert res_high[1].index == 7


if __name__ == '__main__':
    Peak_test()