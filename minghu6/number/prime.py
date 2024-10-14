# -*- coding:utf-8 -*-

from bisect import bisect_left
from heapq import nsmallest
from math import isqrt
from random import randint
from collections.abc import Iterator
from itertools import count, islice, repeat
from typing import Any, NamedTuple
from warnings import warn

from public import public
from bitarray import bitarray

from minghu6.itertools import nth
from minghu6.functools import chain_apply, map, skip, chain


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


@public
def e_sieve(n: int) -> Iterator[int]:
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

    # for i in range(2, n + 1):
    #     if bits[i]:
    #         yield i

    for i, flag in skip(2)(enumerate(bits)):
        if flag:
            yield i


@public
def e_seg_sieve(n: int) -> Iterator[int]:
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

        for i, flag in islice(enumerate(bits), 1, actual_delta + 1):
            if flag:
                yield l + i


@public
def mairson_sieve(n: int) -> Iterator[int]:
    if n == 0:
        return

    right = chain_apply(
        list,
        chain([0]),
        range(1, n + 1)
    )
    left = chain_apply(
        list,
        chain(range(n)),
        [0]
    )

    p = 2
    nsqrt = isqrt(n)

    while p <= nsqrt:
        c = []
        f = p

        while p * f <= n:
            c.append(p * f)
            f = right[f]

        for i in c:
            left[right[i]] = left[i]
            right[left[i]] = right[i]

        p = right[p]

    i = 1

    while right[i] != 0:
        yield right[i]

        i = right[i]


@public
def mairson_sieve_improved(n: int) -> Iterator[int]:
    if n == 0:
        return

    right = chain_apply(
        list,
        chain([0]),
        range(1, n + 1)
    )
    left = chain_apply(
        list,
        chain(range(n)),
        [0]
    )

    p = 2

    f_max = n // 2

    while f_max >= p:
        f = f_max

        while f >= p:
            c = f * p

            right[left[c]] = right[c]
            left[right[c]] = left[c]

            right[c] = n + 1  # mark it
            f = left[f]

        p = right[p]

        if right[f_max] == n + 1:
            f_max = left[f_max]

        while f_max * p > n:
            f_max = left[f_max]

    i = 1

    while right[i] != 0:
        yield right[i]

        i = right[i]


@public
def mairson_dual_sieve(n: int) -> Iterator[int]:
    if n <= 1:
        return

    bits = bitarray(n + 1)
    bits.setall(1)

    pris = []

    for f in range(2, n // 2 + 1):
        if bits[f]:
            pris.append(f)

        for p in pris:
            c = f * p

            if c > n:
                break

            bits[c] = 0

            if f % p == 0:
                break

    yield from pris

    for i in range(n // 2 + 1, n + 1):
        if bits[i]:
            yield i


@public
def mairson_dual_sieve_factorization(n: int) -> tuple[list[int], list[int]]:
    """
    :return: (primes, lpf)
    """

    lpf = [0] * (n + 1)
    pris = []

    if n <= 1:
        return (pris, lpf)

    for f in range(2, n // 2 + 1):
        if lpf[f] == 0:
            lpf[f] = f
            pris.append(f)

        for p in pris:
            c = p * f

            if c > n:
                break

            lpf[c] = p

            if p == lpf[f]:
                break

    for i in range(n // 2 + 1, n + 1):
        if lpf[i] == 0:
            lpf[i] = i
            pris.append(i)

    return (pris, lpf)


@public
def wheel_sieve(n: int) -> Iterator[int]:
    warn("Too Slow", DeprecationWarning)

    class Meta:
        def __init__(self, value: int = 0, left: int = 0, right: int = 0):
            self.value = value
            self.left = left
            self.right = right

    class CompactDoubleList:
        def __init__(self) -> None:
            self.tail: int = 0
            self.arr: list[Meta] = [Meta()]

        def append_value(self, v: int):
            self.arr[self.tail].right = self.tail + 1

            new_node = Meta(v, self.tail, 0)

            if self.tail == len(self.arr) - 1:
                self.arr.append(new_node)
            else:
                self.arr[self.tail + 1] = new_node

            self.tail += 1

        def delete_item(self, meta: Meta):
            left = meta.left
            right = meta.right

            self.arr[left].right = right
            self.arr[right].left = left

        def __iter__(self) -> Iterator[Meta]:
            i = self.arr[0].right

            while i != 0:
                yield self.arr[i]

                i = self.arr[i].right

        def __getitem__(self, i: int) -> int:
            return nth(self, i)

    def rolling(cpl: CompactDoubleList, l: int, n: int):
        for meta in cpl:
            if meta.value + l > n:
                break

            cpl.append_value(meta.value + l)

    def delete_multiple_p(cpl: CompactDoubleList, p: int):
        for meta in cpl:
            if meta.value % p == 0:
                cpl.delete_item(meta)

    if n <= 1:
        return

    p = 3

    w = CompactDoubleList()
    w.append_value(1)

    l = 2
    yield 2

    nsqrt = isqrt(n)

    while p <= nsqrt:
        rolling(w, l, min(p * l, n))
        delete_multiple_p(w, p)

        yield p

        # prevent big int multiple
        l = min(p * l, n)
        p = nth(w, 1).value

    rolling(w, l, n)

    yield from chain_apply(
        map(lambda meta: meta.value),
        skip(1),
        w
    )


class Wheel(NamedTuple):
    """
    :ipm: ordered (f/2)
    """
    w: list[int]
    wg: list[int]
    prod: int
    ipm: list[int]


_WN: int = 5

# top7 primes
_P: list[int] = [
    1,  # just for padding
    2,
    3,
    5,
    7,
    11,
    13,
    17,
]


def _build_wheels(n: int) -> list[Wheel]:
    if n > 7:
        raise ValueError(f"too large wheel size {n}")

    wheels = [
        Wheel([], [], 1, []),
        Wheel([1], [2], 2, [])
    ]

    for k in range(2, n + 1):
        wg0 = wheels[k - 1].wg
        prod0 = wheels[k - 1].prod

        w = []
        acc = 1

        for _ in range(_P[k]):
            for i in range(len(wg0)):
                if acc % _P[k] != 0:
                    w.append(acc)

                acc += wg0[i]

        prod = prod0 * _P[k]

        wg = chain_apply(
            list,
            chain([prod + 1 - w[-1]]),
            map(lambda i: w[i] - w[i - 1]),
            range(1, len(w))
        )

        ipm = chain_apply(
            sorted,
            set,
            map(lambda x: x // 2),
            wg
        )

        wheels.append(Wheel(
            w,
            wg,
            prod,
            ipm
        ))

    return wheels


WHEELS = _build_wheels(_WN)


@public
def fixed_wheel_seg_sieve(n: int) -> Iterator[int]:
    k = _WN
    w, wg, prod, _ = WHEELS[k]
    wsize = len(wg)

    def locate_in_wheel(w: list[int], prod: int, raw: int) -> tuple[int, int]:
        prod_rem = raw % prod
        prod_base = raw - prod_rem

        vi = bisect_left(w, prod_rem)
        v = prod_base + w[vi]

        return (v, vi)

    if n == 0:
        return

    delta = isqrt(n)
    pris = list(e_sieve(delta))

    np = len(pris)

    v = 1 + wg[0]
    vi = 1

    if np <= k:
        # Just rolling to n

        for i in range(1, k + 1):
            if _P[i] > n:
                return

            yield _P[i]

        while v <= n:
            yield v

            v += wg[vi]
            vi = (vi + 1) % wsize

        return

    yield from pris

    # init v, vi

    v_raw = delta + 1
    v, vi = locate_in_wheel(w, prod, v_raw)

    # init factors

    factors = []

    for i in range(np - k):
        p = pris[k + i]
        f_raw = delta // p + 1

        factors.append(locate_in_wheel(w, prod, f_raw))

    # main body

    bits = bitarray(delta + 1)
    bits.setall(1)

    for l in range(delta, n + 1, delta):
        bits.setall(1)
        end = min(l + delta, n)

        # sift for p_k..p_np

        for i in range(np - k):
            p = pris[k + i]
            f, fi = factors[i]

            c = p * f

            while c <= end:
                bits[c - l] = 0

                f += wg[fi]
                fi = (fi + 1) % wsize
                c = p * f

            factors[i] = (f, fi)

        # accumulate primes

        while v <= end:
            if bits[v - l]:
                yield v

            v += wg[vi]
            vi = (vi + 1) % wsize

        # reset for next segment

        bits.setall(1)


@public
def fixed_wheel_seg_sieve_mul2add(n: int) -> Iterator[int]:
    k = _WN
    w, wg, prod, ipm = WHEELS[k]
    wsize = len(wg)

    def locate_in_wheel(w: list[int], prod: int, raw: int) -> tuple[int, int]:
        prod_rem = raw % prod
        prod_base = raw - prod_rem

        vi = bisect_left(w, prod_rem)
        v = prod_base + w[vi]

        return (v, vi)

    if n == 0:
        return

    delta = isqrt(n)
    pris = list(e_sieve(delta))

    np = len(pris)

    v = 1 + wg[0]
    vi = 1

    if np <= k:
        # Just rolling to n

        for i in range(1, k + 1):
            if _P[i] > n:
                return

            yield _P[i]

        while v <= n:
            yield v

            v += wg[vi]
            vi = (vi + 1) % wsize

        return

    yield from pris

    # init v, vi

    v_raw = delta + 1
    v, vi = locate_in_wheel(w, prod, v_raw)

    # init factors and pms

    factors = []
    pms = [[0] * (ipm[-1] + 1) for _ in range(np - k)]

    for i in range(np - k):
        p = pris[k + i]
        f_raw = delta // p + 1

        f, fi = locate_in_wheel(w, prod, f_raw)

        factors.append((p * f, fi))

        # j: half delta_f
        for j in ipm:

            # p * delta_f
            pms[i][j] = j * 2 * p


    # main body

    bits = bitarray(delta + 1)
    bits.setall(1)

    for l in range(delta, n + 1, delta):
        bits.setall(1)
        end = min(l + delta, n)

        # sift for p_k..p_np

        for i in range(np - k):
            p = pris[k + i]
            c, fi = factors[i]

            while c <= end:
                bits[c - l] = 0

                c += pms[i][wg[fi] >> 1]
                fi = (fi + 1) % wsize

            factors[i] = (c, fi)

        # accumulate primes

        while v <= end:
            if bits[v - l]:
                yield v

            v += wg[vi]
            vi = (vi + 1) % wsize

        # reset for next segment

        bits.setall(1)


@public
def sundram_sieve(n: int) -> Iterator[int]:

    if n <= 1:
        return

    k = (n - 1) // 2

    bits = bitarray(k + 1)
    bits.setall(1)

    for i in range(1, k + 1):
        for j in range(i, k + 1):
            odd_base = i + j + 2 * i * j

            if odd_base > k:
                break

            bits[odd_base] = 0

    yield 2

    for i in range(1, k + 1):
        if bits[i]:
            yield 2 * i + 1

    # more slow
    # for i, flag in islice(enumerate(bits), 1, None):
    #     if flag:
    #         yield 2 * i + 1


@public
def sundram_sieve_improved(n: int) -> Iterator[int]:

    if n <= 1:
        return

    k = (n - 1) // 2

    bits = bitarray(k + 1)
    bits.setall(1)

    for odd1 in range(3, isqrt(n) + 1, 2):

        for c in range(odd1 ** 2, n + 1, 2 * odd1):
            bits[(c - 1) // 2] = 0

        # for odd2 in count(odd1, step=2):
        #     c = odd1 * odd2

        #     if c > n:
        #         break

        #     bits[(c - 1) // 2] = 0

    yield 2

    for i in range(1, k + 1):
        if bits[i]:
            yield 2 * i + 1


@public
def atkin_sieve_simple(n: int) -> Iterator[int]:

    if n == 0:
        return

    bits = bitarray(n + 1)

    if n >= 2:
        bits[2] = 1

    if n >= 3:
        bits[3] = 1

    nsqrt = isqrt(n)

    for x in range(1, nsqrt + 1):
        for y in range(1, nsqrt + 1):

            c1 = 4 * x ** 2 + y ** 2

            # not using 2-3-5 wheel sieve for efficiency
            if c1 <= n and c1 % 12 in (1, 5):
                # flip the bit
                bits[c1] ^= 1

            c2 = 3 * x ** 2 + y ** 2

            # 1 mod 6 => 7 mod 12
            # trim duplicate element with algs1

            if c2 <= n and c2 % 12 == 7:
                bits[c2] ^= 1

            if x > y:
                c3 = 3 * x ** 2 - y ** 2

                if c3 <= n and c3 % 12 == 11:
                    bits[c3] ^= 1

    # trim p^2

    for i in range(5, nsqrt + 1):
        if bits[i]:
            r = i ** 2

            for j in range(r, n + 1, r):
                bits[j] = 0

    for i in range(1, n + 1):
        if bits[i]:
            yield i


@public
def gpf_sieve(n: int) -> Iterator[int]:
    if n <= 1:
        return

    p = 2

    bits = bitarray(n + 1)
    bits.setall(1)

    factors = []

    i = 2

    while p <= (n >> 1):

        yield p

        factors.append(p)

        f_stack = factors
        factors = []

        while f_stack:
            f = f_stack.pop()
            c = p * f

            if c <= n:
                bits[c] = 0

                f_stack.append(c)
                factors.append(f)

        i += 1

        while not bits[i]:
            i += 1

        p = i

    for i in range(n // 2 + 1, n + 1):
        if bits[i]:
            yield i


@public
def e_sieve_inf() -> Iterator[int]:

    pris = [2]

    p1 = pris[0]
    l0 = p1
    l1 = p1 * p1
    delta = l1 - l0
    seg = bitarray(delta + 1)
    seg.setall(1)

    yield from pris

    while True:
        for p in pris:
            for i in range(p - l0 % p, delta + 1, p):
                seg[i] = 0

        for i in range(1, delta + 1):
            if seg[i]:
                p = l0 + i

                yield p

                pris.append(p)

        l0 = l1
        p1 = pris[-1]
        l1 = p1 ** 2
        delta0 = delta
        delta = l1 - l0

        seg.extend(repeat(1, times=delta - delta0))
        seg.setall(1)


@public
def gpf_sieve_inf() -> Iterator[int]:
    """ *LINEAR PRIME-NUMBER SIEVES: A FAMILY TREE:* Algorithm 4.4. """

    lastp = 2
    sqrtp = 2
    gpf = [0] * (2 * 2 + 1)

    yield 2

    for n in count(3):
        if n == sqrtp ** 2:
            gpf[n] = sqrtp      # add starter
            sqrtp = gpf[sqrtp]  # point to next prime after sqrtp

        if gpf[n] == 0:
            yield n

            gpf[lastp] = n
            lastp = n
            gpf.extend(repeat(0, times=4 * n - len(gpf)))

        else:
            p = gpf[n]
            f = n // p
            p1 = gpf[p]  # next prime

            gpf[p1 * f] = p1

            if p == min(f, gpf[f]):
                f0 = f // p + 1

                while min(f0, gpf[f0]) > p:
                    f0 += 1

                gpf[f0 * p * p] = p


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
    # 247 nonprime
    print(list(islice(e_sieve_inf(), 10)))
