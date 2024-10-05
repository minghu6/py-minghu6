from collections.abc import Callable
from itertools import tee
from types import ModuleType
from typing import NamedTuple

from minghu6.functools import chain_apply, map, filter

BENCHES_SLOT = "__m6_benches__"

type BenchCase = Callable[[], None]

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
#### Runner


def simplify_time_ns(ns: int) -> tuple[int, int, str]:
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

def bench_on_module(m: ModuleType, casenames=list[str] | None):
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

    if not benches:
        print(f"No bench case found on `{m.__name__}`")

        return

    class CaseStats(NamedTuple):
        """case -> module -> benchmark -(archiving)> records"""

        fname: str
        ave: float
        iters: int

    module_stats: list[CaseStats] = []

    for f in benches:
        from timeit import Timer

        t = Timer(f"{f.__name__}()", globals=m.__dict__)

        iters: int
        secs: float
        iters, secs = t.autorange()

        nanos = int(secs * 10**9)
        ave = nanos // iters

        fname = f.__name__

        module_stats.append(CaseStats(fname, ave, iters))

    # formatted output

    max_fn_len = chain_apply(max, map(lambda f: len(f.__name__)), benches)

    min_ave_time, max_ave_time = chain_apply(
        lambda g: (min(g[0]), max(g[1])),
        tee,
        map(lambda stats: stats.ave),
        module_stats,
    )

    _, multiple, unit = simplify_time_ns(min_ave_time)

    max_ave_time_len = len(f"{max_ave_time/multiple :> ,.1f} {unit}")

    print(f"\nrunning on `{m.__name__}`:\n")

    for stats in module_stats:
        print(
            f"{' ':5}{stats.fname:<{max_fn_len +1}} ... "
            f"{stats.ave/multiple :> {max_ave_time_len+1},.1f} {unit} "
            f"({stats.iters:,} iters)"
        )
