# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def allis_test():
    from minghu6.algs.var import allis


def isnum_str_test():
    from minghu6.algs.var import isnum_str

    assert isnum_str('1023') == True

    assert isnum_str('1ab2') == False




if __name__ == '__main__':

    allis_test()
