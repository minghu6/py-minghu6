# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def issquare(n):
    """
    :param n:
    :return:
    >>> issquare(256)
    True
    >>> issquare(255)
    False
    """
    i = 1
    while n > 0:
        n -= i
        i += 2

    return n == 0

if __name__ == '__main__':

    import doctest

    doctest.testmod()