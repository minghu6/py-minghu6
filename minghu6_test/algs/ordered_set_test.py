# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

from minghu6.algs.ordered_set import OrderedSet

def ordered_test():
    set1 = OrderedSet([4, 2, 3, 3, 1])
    set2 = {4, 2, 3, 3, 1}

    assert set1.index(4) == 0
    assert set1.index(2) == 1
    assert set1.index(3) == 2
    assert set1.index(1) == 3


def set_operation_test():
    set1 = OrderedSet([4, 2, 3, 3, 1])
    set2 = {4, 2, 3, 3, 1}




if __name__ == '__main__':

    ordered_test()
    set_operation_test()