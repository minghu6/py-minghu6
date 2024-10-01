# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from math import isqrt
import random
from typing import Iterator, List
from itertools import count


def isprime(n):
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i <= isqrt(n):
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def lpf(n):
    """Least Prime Factor of Number"""

    if n == 0 or n == 1:
        return n

    if n % 2 == 0:
        return 2
    elif n % 3 == 0:
        return 4

    i = 5
    while i <= isqrt(n):
        if n % i == 0 or n % (i + 2) == 0:
            return i

        i += 6

    return n


def find_prime_random(end, start=0):
    while True:
        # Select a random number n
        n = random.randint(start, end)
        # print(n)
        if isprime(n):
            return n


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


def factorization(n: int) -> List[int]:
    """(prime) factorization

    >>> factorization(28)
    [2, 2, 7]
    >>> factorization(0)
    []
    >>> factorization(1)
    []
    """

    if n == 0 or n == 1:
        return []

    factors = []

    for p in bengelloun_sieve_inf():
        if n == 1:
            return factors

        while n % p == 0:
            n //= p

            factors.append(p)


if __name__ == "__main__":
    n = find_prime_random(1024)
    print(n)
