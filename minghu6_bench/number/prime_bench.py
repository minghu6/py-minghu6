from cProfile import Profile
from pstats import SortKey
from collections.abc import Callable, Generator

from pprint import pprint
from minghu6.number.prime import *
from minghu6.test.bench import bench, BENCHES_SLOT

type Sieve = Callable[[int], Generator[int, None, None]]
type SieveInf = Callable[[], Generator[int, None, None]]

################################################################################
#### Profile

def profile_sieve_inf(f: SieveInf, n=169_000):
    print(f"\nProfile `{f.__name__}`:\n")
    with Profile() as pr:
        for p in f():
            if p > n:
                break

        pr.print_stats(sort=SortKey.CUMULATIVE)


def profile_sieve(f: Sieve, n = 169_000):
    print(f"\nProfile `{f.__name__}`:\n")

    with Profile() as pr:
        for _p in f(n):
            pass

        pr.print_stats(sort=SortKey.CUMULATIVE)

################################################################################
#### Bench

SIEVE_BENCH_N = 169_000

def bench_sieve(f: Sieve):
    for _ in f(SIEVE_BENCH_N):
        pass

def bench_sieve_inf(f: SieveInf):
    for p in f():
        if p > SIEVE_BENCH_N:
            break

@bench
def bench_e_sieve():
    bench_sieve(e_sieve)

@bench
def bench_e_seg_sieve():
    bench_sieve(e_seg_sieve)

@bench
def bench_bengelloun_sieve_inf():
    bench_sieve_inf(bengelloun_sieve_inf)


if __name__ == "__main__":

    profile_sieve_inf(bengelloun_sieve_inf)
    profile_sieve(e_sieve)
    profile_sieve(e_seg_sieve)
