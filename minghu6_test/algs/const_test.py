# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def const_test():
    from minghu6.algs import const

    const.SUCCESSFUL_UPPER_EXAMPLE = 1
    try:
        const.failed_lower_example = 1
    except Exception as ex:
        print(ex)




if __name__ == '__main__':
    const_test()