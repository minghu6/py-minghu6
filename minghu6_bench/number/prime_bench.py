from cProfile import Profile
from pstats import SortKey
from collections.abc import Callable, Generator

from minghu6.number.prime import *
from minghu6.test.bench import bench, skip


type Sieve = Callable[[int], Generator[int, None, None]]
type SieveInf = Callable[[], Generator[int, None, None]]

################################################################################
#### Profile

SIEVE_PROFILE_N = 169_000

def profile_sieve_inf(f: SieveInf, n=SIEVE_PROFILE_N):
    print(f"\nProfile `{f.__name__}`:\n")
    with Profile() as pr:
        for p in f():
            if p > n:
                break

        pr.print_stats(sort=SortKey.CUMULATIVE)


def profile_sieve(f: Sieve, n=SIEVE_PROFILE_N):
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
def bench_mairson_sieve():
    bench_sieve(mairson_sieve)

@skip('same with mairson_sieve')
@bench
def bench_mairson_sieve_improved():
    bench_sieve(mairson_sieve_improved)

@bench
def bench_mairson_dual_sieve():
    bench_sieve(mairson_dual_sieve)

@bench
def bench_mairson_dual_sieve_factorization():
    bench_sieve(mairson_dual_sieve_factorization)

@skip('slow')
@bench
def bench_wheel_sieve():
    bench_sieve(wheel_sieve)

@bench
def bench_sfws_sieve():
    bench_sieve(fixed_wheel_seg_sieve)

@bench
def bench_sfws_mul2add_sieve():
    bench_sieve(fixed_wheel_seg_sieve_mul2add)

@skip('slow')
@bench
def bench_sundaram_sieve():
    bench_sieve(sundram_sieve)

@bench
def bench_sundaram_sieve_improved():
    bench_sieve(sundram_sieve_improved)

@skip('slow')
@bench
def bench_atkin_sieve_simple():
    bench_sieve(atkin_sieve_simple)

@skip('slow')
@bench
def bench_gpf_sieve():
    bench_sieve(gpf_sieve)

@skip('slow')
@bench
def bench_bengelloun_sieve_inf():
    bench_sieve_inf(bengelloun_sieve_inf)

@skip('slow')
@bench
def bench_e_sieve_inf():
    bench_sieve_inf(e_sieve_inf)


if __name__ == "__main__":

    profile_sieve_inf(bengelloun_sieve_inf)
    profile_sieve(e_sieve)
    profile_sieve(e_seg_sieve)
