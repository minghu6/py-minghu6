

from cProfile import Profile
from pstats import SortKey

from minghu6.test.bench import BenchCase, run_a_benchmark
from minghu6.test.profile import Watch
from minghu6_bench.number.prime_bench import bench_mairson_sieve


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

if __name__ == '__main__':

    # profile_run_a_benchmark(bench_mairson_sieve)

    profile_watch(bench_mairson_sieve)
