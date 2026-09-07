from cProfile import Profile
from pstats import SortKey

from minghu6.test.bench import BenchCase, run_a_benchmark
from minghu6.test.profile import Watch

# from ..number.bench_prime import mairson_sieve


def profile_run_a_benchmark(f: BenchCase):
    print(f"\nProfile `run_a_benchmark({f.__name__})`:\n")

    with Profile() as pr:
        run_a_benchmark(f)

        pr.print_stats(sort=SortKey.CUMULATIVE)


def profile_watch(f: BenchCase):
    print(f"\nProfile `Watch({f.__name__})`:\n")

    with Profile() as pr:
        with Watch() as w:
            f()

        pr.print_stats(sort=SortKey.CUMULATIVE)


if __name__ == "__main__":
    from minghu6.number.prime import mairson_sieve

    SIEVE_BENCH_N = 169_000

    def bench_sieve(f):
        for _ in f(SIEVE_BENCH_N):
            pass

    def bench_mairson_sieve():
        bench_sieve(mairson_sieve)

    # profile_run_a_benchmark(bench_mairson_sieve)
    profile_watch(bench_mairson_sieve)
