from collections.abc import Callable
from datetime import datetime
from functools import cache
from itertools import tee
from numbers import Number
from os import PathLike
from pathlib import Path
from statistics import mean, median
from types import ModuleType
from typing import Iterator, List, NamedTuple, Union
import sys, importlib.util, re, keyword

from exports import export

from minghu6.functools import compose, fmap, keep
from minghu6.stats import median_abs_dev, winsoring
from minghu6.test.profile import Watch


BENCHES_SLOT = "__m6_benches__"
BENCH_META_SLOT = "__m6_bench_meta__"

PUBLIC_IDENTIFIER = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
BENCH_PRIVATE_ROOT_PACKAGE = "_virtual_bench_m6"


type BenchCase = Callable[[], None]
type BenchCaseDecorator = Callable[[BenchCase], BenchCase]
type BenchRunner = Callable[[BenchCase], ModuleStats]
type StrPath = Union[str, PathLike[str]]

################################################################################
#### Tag Benchmark Target

@export
class BenchMetaSlotOverridedError(Exception):
    pass


@export
class BenchMetaSlotNotFoundError(Exception):
    pass


class BenchMeta:
    def __init__(self) -> None:
        self.skipped = False

def _meta(o: object) -> BenchMeta | None:
    """ Bench Meta Reader """

    return getattr(o, BENCH_META_SLOT, None)


@export
def skip(reason: str | None = None) -> BenchCaseDecorator:
    def _skip(f: BenchCase) -> BenchCase:
        if not isinstance(_meta(f), BenchMeta):
            raise BenchMetaSlotNotFoundError(
                "`@skip()` should work with `@bench`"
            )

        _meta(f).skipped = True

        return f

    return _skip


@export
def bench(f: BenchCase) -> BenchCase:
    """
    Decorators for function to bench
    saving in `module.__m6_benches__: list[Callable[]]`
    """

    # the global namespace of the module which holds `f`
    g = f.__globals__

    if _meta(f) is not None:
        raise BenchMetaSlotOverridedError(
            f"{BENCH_META_SLOT}"
        )

    setattr(f, BENCH_META_SLOT, BenchMeta())

    if BENCHES_SLOT not in g:
        g[BENCHES_SLOT] = [f]
    else:
        g[BENCHES_SLOT].append(f)

    return f


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
            compose(
                keep(
                    lambda f: any(
                        map(lambda name: name in f.__name__, casenames)
                    )
                ),
                benches,
            )
        )

    # skip `skipped`

    benches = list(
        compose(
            keep(
                lambda f: not _meta(f).skipped
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
    # total nano seconds
    wall: int


class ModuleStats(NamedTuple):
    mname: str
    cstats_list: list[CaseStats]
    # total nano seconds
    wall: int  # sum of `CaseStats.wall`

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


def stats_sample2case(f: BenchCase, stats: SampleStats, wall: int) -> CaseStats:
    """ Convert `SampleStats` to `CaseStats` """

    return CaseStats(
        fname=f.__name__,
        ave=stats.median,
        iters=stats.n,
        dev=int(stats.max - stats.min),
        raw_samples=stats.samples,
        wall=wall
    )


@export
def classic_run_a_benchmark(f: BenchCase) -> CaseStats:
    def _classic_run_a_benchmark(f: BenchCase) -> CaseStats:
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
            raw_samples=samples,
            wall=0
        )

    with Watch() as w:
        stats = _classic_run_a_benchmark(f)

    stats.wall = w.nanos

    return stats


@export
def run_a_benchmark(f: BenchCase) -> CaseStats:
    def _run_a_benchmark(f: BenchCase) -> SampleStats:
        with Watch() as w:
            f()

        tot = w.nanos

        if w.nanos == 0:
            raise RuntimeError("It's just impossible for CPython")

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

    with Watch() as w:
        stats = _run_a_benchmark(f)

    return stats_sample2case(f, stats, w.nanos)


################################################################################
#### Output

def simplify_sampling_time(ns: int) -> tuple[int, int, str]:
    """
    :return: (time, multiple, unit)
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


def fmt_wall_time(ns: int) -> str:
    if ns >= 3_600_000_000_000:          # >= 1 h
        h, rem = divmod(ns, 3_600_000_000_000)
        m = rem // 60_000_000_000

        return f"{h}h {m}min"

    if ns >= 60_000_000_000:             # >= 1 min
        m, rem = divmod(ns, 60_000_000_000)
        s = round(rem / 1_000_000_000)

        return f"{m}min {s}s"

    if ns >= 1_000_000_000:              # >= 1 s
        return f"{ns / 1_000_000_000:.2f}s"

    return f"{ns / 1_000_000:.2f}ms"     # down to ms


def output_console(mstats: ModuleStats):
    shown_mname = mstats.mname.removeprefix(f"{BENCH_PRIVATE_ROOT_PACKAGE}.")

    if not mstats.cstats_list:
        print(f"No bench case found on `{shown_mname}`")
        return

    max_fn_len = compose(
        max,
        fmap(lambda stats: len(stats.fname)),
        mstats
    )

    min_ave_time, max_ave_time = compose(
        lambda g: (min(g[0]), max(g[1])),
        tee,
        fmap(lambda stats: stats.ave),
        mstats,
    )

    _, multiple, unit = simplify_sampling_time(min_ave_time)

    max_dev_time = compose(
        max,
        fmap(lambda stats: stats.dev),
        mstats
    )

    max_iters = compose(
        max,
        fmap(lambda stats: stats.iters),
        mstats
    )

    max_ave_time_len = len(f"{max_ave_time / multiple:,.2f}")
    max_dev_time_len = len(f"{max_dev_time / multiple:,.2f}")
    max_iters_len = len(f"{max_iters:,}")

    print(f"\nrunning on `{shown_mname}`:\n")

    for stats in mstats:
        print(
            f"{' ':5}{stats.fname:<{max_fn_len + 1}} ... "
            f"{stats.ave / multiple:>{max_ave_time_len + 1},.2f} {unit} "
            f"({stats.iters:>{max_iters_len + 1},} iters) "
            f"(+/- {stats.dev / multiple:>{max_dev_time_len + 1},.2f} {unit})"
        )

    print()
    print(f"finished in {fmt_wall_time(mstats.wall)}.")

################################################################################
#### Runner

@export
def bench_on_module(
    m: ModuleType, casenames=list[str] | None, output=output_console,
    runner: BenchRunner = run_a_benchmark
):
    """
    :spec_names: support partial match on casenames
    """

    benches = collect_benchmarks(m, casenames=casenames)
    cstats = [runner(f) for f in benches]

    mstats = ModuleStats(
        m.__name__,
        cstats,
        wall=sum(stats.wall for stats in cstats)
    )

    output(mstats)



def relpath2modname(fullpath: Path, basepath: Path) -> str:
    assert fullpath.suffixes == [".py"] or not fullpath.suffixes

    parts = list(fullpath.relative_to(basepath).parts)

    parts[-1] = parts[-1].removesuffix(".py")

    return '.'.join(parts)


def load_script(path: StrPath, base: StrPath | None) -> ModuleType:
    """Load a script file as a module.
    """

    path = Path(path)

    if base:
        partmodname = relpath2modname(path, Path(base))
    else:
        partmodname = path.stem

    fullmodname = f"{BENCH_PRIVATE_ROOT_PACKAGE}.{partmodname}"

    spec = importlib.util.spec_from_file_location(
        fullmodname,
        path,
        submodule_search_locations=[str(path.parent)]
    )
    module = importlib.util.module_from_spec(spec)
    module.__package__ = fullmodname.rsplit('.', 1)[0]
    sys.modules[fullmodname] = module
    spec.loader.exec_module(module)

    return module


@export
def public_modname_from_folder(name: str) -> str | None:
    modname = name.replace('-', '_')

    if PUBLIC_IDENTIFIER.match(modname) and not keyword.iskeyword(modname):
        return modname


def scan_virtual_packages(base: Path) -> Iterator[(Path, str)]:
    """Top-down find all valid module folder.
    :yield: For `base/foo/bar` it yields (Path("foo/bar"), 'foo.bar')
    """

    for root, dirs, _ in base.walk(top_down=True):
        valid_dirs = []

        for dirname in dirs:
            if bool(modname := public_modname_from_folder(dirname)):
                valid_dirs.append(modname)

        for dirname in valid_dirs:
            fullpath = Path(root) / dirname
            fullmodname = relpath2modname(fullpath, base)

            yield (fullpath, fullmodname)

        dirs[:] = valid_dirs


def register_virtual_package(path: Path, fullmodname: str):
    if fullmodname in sys.modules:
        raise ValueError(
            f"Module '{fullmodname}' already exists in sys.modules"
        )

    init_file_path = path / "__init__.py"

    if init_file_path.exists():
        spec = importlib.util.spec_from_file_location(
            fullmodname,
            init_file_path,
            submodule_search_locations=[str(path)]
        )
    else:
        spec = importlib.util.spec_from_loader(
            fullmodname,
            None,
            is_package=True
        )
        spec.submodule_search_locations = [str(path)]

    module = importlib.util.module_from_spec(spec)
    module.__package__ = fullmodname
    # unload old module if exists
    sys.modules.pop(fullmodname, None)
    sys.modules[fullmodname] = module


def discover_virtual_packages(base_path: StrPath):
    base_path = Path(base_path)

    register_virtual_package(base_path, BENCH_PRIVATE_ROOT_PACKAGE)

    for pkg_path, pkg_name in scan_virtual_packages(base_path):
        register_virtual_package(pkg_path, f"{BENCH_PRIVATE_ROOT_PACKAGE}.{pkg_name}")


@export
def bench_on_script(
    m: ModuleType, casenames=list[str] | None, output=output_console,
    runner: BenchRunner = run_a_benchmark
):

    pass
