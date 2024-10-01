#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def fast_exp_mod(b, e, m):
    """
    e = e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n)

    b^e = b^(e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n))
        = b^(e0*(2^0)) * b^(e1*(2^1)) * b^(e2*(2^2)) * ... * b^(en*(2^n))

    b^e mod m = ((b^(e0*(2^0)) mod m) * (b^(e1*(2^1)) mod m) * (b^(e2*(2^2)) mod m) * ... * (b^(en*(2^n)) mod m) mod m

    return b^e mod m
    """
    result = 1
    while e != 0:
        if (int(e) & 1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e = int(e) >> 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b * b) % m
    return result


try:
    from math import gcd
except ImportError:

    def gcd(m, n):
        """
        >>> gcd(1920, 1080)
        120
        :param m:
        :param n:
        :return:
        """
        assert isinstance(m, int)
        assert isinstance(n, int)
        m = abs(m)
        n = abs(n)

        if m < n:
            smaller_num = m
        else:
            smaller_num = n
        for i in range(smaller_num, 0, -1):
            if m % i == 0 and n % i == 0:
                return i

else:
    pass


def lcm(m, n):
    assert isinstance(m, int)
    assert isinstance(n, int)
    return (m * n) / gcd(m, n)


def simpleist_int_ratio(m, n):
    """
    >>> simpleist_int_ratio(1920, 1080)
    (16, 9)
    """
    m = int(m)
    n = int(n)
    gcd_num = gcd(m, n)
    return m // gcd_num, n // gcd_num


def is_power_2_natrual(n):
    """
    only for Natural number 1,+2,+4,+8,...
    """
    if not isinstance(n, int) or n <= 0:
        raise Exception('Not an Natural Number')

    return not (n & (n - 1))


def is_power(n, m):
    """
    judge if n is power of m;(n>0,m>1)
    """
    import math
    result = math.log(m, n)

    if m <= 1 or n <= 0:
        raise Exception('\n\tInvalid parameter ! \n\tBe Sure:p1>0 p2>1')
    return int(result) == result


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

