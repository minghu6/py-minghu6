from cProfile import Profile
from pstats import SortKey
from collections.abc import Callable, Generator

from minghu6.number.prime import *

type Sieve = Callable[[int], Generator[int, None, None]]
type SieveInf = Callable[[], Generator[int, None, None]]


def profile_sieve_inf(f: SieveInf, n=1_000_000):
    print(f"Profile <{f.__name__}>:")
    print()
    with Profile() as pr:
        for p in f():
            if p > n:
                break

        pr.print_stats(sort=SortKey.CUMULATIVE)


def profile_sieve(f: Sieve, n = 169_000):
    print(f"Profile <{f.__name__}>:")
    print()

    with Profile() as pr:
        for _p in f(n):
            pass

        pr.print_stats(sort=SortKey.CUMULATIVE)


if __name__ == "__main__":
    # profile_sieve_inf(bengelloun_sieve_inf)

    # profile_sieve(e_sieve_seg)

    import timeit

    print(timeit.timeit("e_sieve(100_000)", globals=locals()))
