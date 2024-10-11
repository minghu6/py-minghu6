from collections.abc import Callable
from functools import cache
from itertools import tee
from numbers import Number
from statistics import mean, median
import time
from types import ModuleType
from typing import NamedTuple

from minghu6.functools import chain_apply, map, filter
from minghu6.stats import median_abs_dev, winsoring

BENCHES_SLOT = "__m6_benches__"

type BenchCase = Callable[[], None]
type BenchRunner = Callable[[BenchCase], ModuleStats]

################################################################################
#### Decorators


def bench(f: BenchCase) -> BenchCase:
    """
    Decorators for function to bench
    saving in `module.__m6_benches__: list[Callable[]]`
    """

    # the global namespace of the module which holds `f`
    g = f.__globals__

    if BENCHES_SLOT not in g:
        g[BENCHES_SLOT] = [f]
    else:
        g[BENCHES_SLOT].append(f)

    return f

################################################################################
#### Context Manager


class Watch:
    def __init__(self, fmt=".2f") -> None:
        """
        :fmt: format float number of (s/ms/us)
        """
        self.fmt = fmt

    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter_ns()
        self._nanos = self.end - self.start

    @property
    def nanos(self) -> int:
        return self._nanos

    @property
    def micros(self) -> float:
        return self._nanos / 1000

    @property
    def millis(self) -> float:
        return self._nanos / 1000_000

    @property
    def secs(self) -> float:
        return self._nanos / 1000_000_000

    def __str__(self) -> str:
        lit, _, unit = _simplify_time_ns(self._nanos)

        return f"{lit:{self.fmt}} {unit}"


################################################################################
#### Collector

def collect_benchmarks(
    m: ModuleType, casenames=list[str] | None
) -> list[BenchCase]:
    """
    :spec_names: support partial match on casenames
    """

    benches: list[BenchCase] = getattr(m, BENCHES_SLOT, [])

    if casenames:
        benches = list(
            chain_apply(
                filter(
                    lambda f: any(
                        map(lambda name: name in f.__name__)(casenames)
                    )
                ),
                benches,
            )
        )

    return benches


################################################################################
#### Stats Data

class SampleStats:
    def __init__(self, samples: list[Number], n: int):
        self.samples = samples
        self.n = n

    @property
    @cache
    def max(self) -> Number:
        return max(self.samples)

    @property
    @cache
    def min(self) -> Number:
        return min(self.samples)

    @property
    @cache
    def median(self) -> Number:
        return median(self.samples)

    @property
    @cache
    def median_abs_dev(self) -> Number:
        return median_abs_dev(self.samples)

    @property
    @cache
    def median_abs_dev_pct(self) -> Number:
        """ 0.01 stand for 1% """

        return self.median_abs_dev / self.median


class CaseStats(NamedTuple):
    """case -> module -> benchmark -(archiving)> records"""

    fname: str
    ave: int
    iters: int
    # diviation in nanos
    dev: int
    raw_samples: list[Number]


class ModuleStats(NamedTuple):
    mname: str
    cstats_list: list[CaseStats]

    def __iter__(self):
        return iter(self.cstats_list)


################################################################################
#### Bencher

SAMPLE_SIZE: int = 50
WINSORING_PERCENTILE: dict[str, int] = {'n': 100, 'e': 5}


def sampling(f: BenchCase, n: int) -> SampleStats:
    samples = [0] * SAMPLE_SIZE

    for i in range(SAMPLE_SIZE):
        with Watch() as w:
            for _ in range(n):
                f()

        samples[i] = w.nanos // n

    winsoring(samples, **WINSORING_PERCENTILE)

    return SampleStats(samples, n)


def _stats_sample2case(f: BenchCase, stats: SampleStats) -> CaseStats:
    """ Convert `SampleStats` to `CaseStats` """

    return CaseStats(
        fname=f.__name__,
        ave=stats.median,
        iters=stats.n,
        dev=int(stats.max - stats.min),
        raw_samples=stats.samples
    )


def classic_run_a_benchmark(f: BenchCase) -> CaseStats:
    from importlib import import_module
    from timeit import Timer

    samples = [0] * SAMPLE_SIZE
    iters_list = [0] * SAMPLE_SIZE

    for i in range(SAMPLE_SIZE):
        t = Timer(f"{f.__name__}()", globals=import_module(
            f.__module__).__dict__)

        iters: int
        secs: float
        iters, secs = t.autorange()

        samples[i] = int(secs * 1000_000_000 // iters)
        iters_list[i] = iters

    return CaseStats(
        fname=f.__name__,
        ave=mean(samples),
        iters=int(median(iters_list)),
        dev=max(samples) - min(samples),
        raw_samples=samples
    )


def run_a_benchmark(f: BenchCase) -> CaseStats:
    def _run_a_benchmark(f: BenchCase) -> SampleStats:
        with Watch() as w:
            f()

        tot = w.nanos

        assert w.nanos > 0, f"It's just impossible for CPython"

        n = int(max(1000_000 / w.nanos, 1))

        while True:
            with Watch() as w:
                summ = sampling(f, n=n)
                summ5 = sampling(f, n=5 * n)

            if (w.millis > 200
                and summ.median_abs_dev_pct < 1.0
                    and summ.median - summ5.median < summ5.median_abs_dev):

                return summ5

            tot += w.nanos

            if tot > 3_000_000_000:  # 3 seconds
                return summ5

            n *= 10  # x2 x5

    stats = _run_a_benchmark(f)

    return _stats_sample2case(f, stats)


################################################################################
#### Output

def _simplify_time_ns(ns: int) -> tuple[int, int, str]:
    """
    :return: (newint, multiple, unit)
    """

    units = ["us", "ms", "s"]

    t = ns
    multiple = 1
    unit = "ns"

    for _unit in units:
        if t < 1000:
            break

        t /= 1000
        multiple *= 1000
        unit = _unit

    return (t, multiple, unit)


def output_console(mstats: ModuleStats):
    max_fn_len = chain_apply(
        max,
        map(lambda stats: len(stats.fname)),
        mstats
    )

    min_ave_time, max_ave_time = chain_apply(
        lambda g: (min(g[0]), max(g[1])),
        tee,
        map(lambda stats: stats.ave),
        mstats,
    )

    _, multiple, unit = _simplify_time_ns(min_ave_time)

    max_dev_time = chain_apply(
        max,
        map(lambda stats: stats.dev),
        mstats
    )

    max_iters = chain_apply(
        max,
        map(lambda stats: stats.iters),
        mstats
    )

    max_ave_time_len = len(f"{max_ave_time / multiple:,.2f}")
    max_dev_time_len = len(f"{max_dev_time / multiple:,.2f}")
    max_iters_len = len(f"{max_iters:,}")

    print(f"\nrunning on `{mstats.mname}`:\n")

    for stats in mstats:
        print(
            f"{' ':5}{stats.fname:<{max_fn_len + 1}} ... "
            f"{stats.ave / multiple:>{max_ave_time_len + 1},.2f} {unit} "
            f"({stats.iters:>{max_iters_len + 1},} iters) "
            f"(+/- {stats.dev / multiple:>{max_dev_time_len + 1},.2f} {unit})"
        )


################################################################################
#### Runner


def bench_on_module(
    m: ModuleType, casenames=list[str] | None, output=output_console,
    runner: BenchRunner = run_a_benchmark
):
    """
    :spec_names: support partial match on casenames
    """

    benches = collect_benchmarks(m, casenames=casenames)

    if not benches:
        print(f"No bench case found on `{m.__name__}`")

        return

    mstats = ModuleStats(m.__name__, [runner(f) for f in benches])

    output(mstats)
