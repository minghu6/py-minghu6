# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.algs import var

def allis_test():
    from minghu6.algs.var import allis

def allequal_test():
    assert var.allequal([11, 12, 13], (11, 12, 13)) == True
    assert var.allequal([11, 12, 13], [11, 12, 14]) == False

def isnum_str_test():
    from minghu6.algs.var import isnum_str

    assert isnum_str('1023') == True

    assert isnum_str('1ab2') == False




if __name__ == '__main__':

    allis_test()
    allequal_test()
    isnum_str_test()
