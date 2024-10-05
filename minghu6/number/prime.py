# -*- coding:utf-8 -*-

from math import isqrt
from random import randint
from collections.abc import Generator, Iterator
from itertools import count

from public import public
from bitarray import bitarray


@public
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

@public
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

@public
def find_prime_random(end, start=0):
    while True:
        # Select a random number n
        n = randint(start, end)
        # print(n)
        if isprime(n):
            return n


_P = [
    2,
    3,
    5,
    7,
]


def _early_edge_cases(n: int) -> Generator[int, None, None]:
    assert n <= 4

    p0 = [0, 0, 2, 3, 4]

    for i in range(1, n + 1):
        if p0[i]:
            yield i

@public
def e_sieve(n: int) -> Generator[int, None, None]:
    """Eratosenes Sieve
    >>> list(e_sieve(0))
    []
    >>> list(e_sieve(2))
    [2]
    >>> list(e_sieve(3))
    [2, 3]
    """

    bits = bitarray(n + 1)
    bits.setall(1)

    for i in range(2, isqrt(n) + 1):
        if bits[i]:
            for j in range(i * i, n + 1, i):
                bits[j] = 0

    for i in range(2, n + 1):
        if bits[i]:
            yield i

@public
def e_seg_sieve(n: int) -> Generator[int, None, None]:
    """Segmented Eratosenes Sieve"""

    if n <= 1:
        return

    nsqrt = isqrt(n)

    delta = nsqrt

    pris = list(e_sieve(delta))

    yield from pris

    bits = bitarray(delta + 1)

    # (l, l+delta]
    for l in range(delta, n + 1, delta):
        bits.setall(1)
        actual_delta = min(delta, n - l)

        for p in pris:
            i = p - l % p

            for j in range(i, actual_delta + 1, p):
                bits[j] = 0

        for i in range(1, actual_delta + 1):
            if bits[i]:
                yield l + i

@public
def bengelloun_sieve_inf() -> Iterator[int]:
    lastp = 2
    lpf: list[int] = [0] * 5

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

@public
def factorization(n: int) -> list[int]:
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
