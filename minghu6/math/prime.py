# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

import random
from typing import Iterator, List
from itertools import count

__all__ = ["fast_exp_mod", "isprime", "find_prime_random", "simpleist_int_ratio"]


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


def isprime(n):
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i**2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def find_prime_random(end, start=0):
    while True:
        # Select a random number n
        n = random.randint(start, end)
        # print(n)
        if isprime(n):
            return n


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
    :param m:
    :param n:
    :return:
    """
    m = int(m)
    n = int(n)
    gcd_num = gcd(m, n)
    return m // gcd_num, n // gcd_num


def bengelloun_sieve_inf() -> Iterator[int]:
    lastp = 2
    lpf: List[int] = [0] * 5

    yield lastp

    for n in count(3):
        if n % 2 == 0:
            lpf[n] = 2
            lpf[n // 2 * 3] = 3
        elif lpf[n] == 0:
            lpf[lastp] = n
            lastp = n

            yield n

            lpf.extend([0] * (4 * n - len(lpf)))
        else:
            lp0 = lpf[n]
            f = n // lp0

            if lp0 < (lpf[f] if lpf[f] < f else f):
                lp1 = lpf[lp0]
                lpf[lp1 * f] = lp1



if __name__ == "__main__":
    n = find_prime_random(1024)
    print(n)
