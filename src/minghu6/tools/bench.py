"""Bench

running benchmarks of a module.

Usage:
  bench -m <module-name> [-c=<case-name>]... [--classic-runner]
  bench [-B=<base-dir>] [-r] <bench-path>... [-c=<case-name>]... [--classic-runner]

Options:
  <bench-path>                 path to a benchmark file, directory or script file.
                               program will search valid python files whose name start with `bench_`
                               or end with `_bench` in given directories.
  -c, --case-name=<case-name>  case name to run, if not given, all cases will be run (only support partial match).
  -B,--base-dir=<base-dir>     root package to search for benchmarks (used for benchmark script relative import).
  --classic-runner             use Python `Timer::autorange` as benche_runner
"""

from importlib import import_module
from pathlib import Path
from types import ModuleType
from docopt import docopt


import minghu6
from minghu6.test.bench import (
    BenchRunner,
    bench_on_module,
    classic_run_a_benchmark,
    load_script,
    run_a_benchmark,
    discover_virtual_packages,
    public_modname_from_folder
)
from minghu6.test.profile import Watch



def collect_bench_files(paths: list[str], recursive: bool) -> list[Path]:
    bench_files = {}

    for p in paths:
        p = Path(p)

        if not p.exists():
            raise FileNotFoundError(f"Path '{p}' does not exist")

        if p.is_dir():
            entries = p.rglob('*.py') if recursive else p.glob('*.py')

            for entry in entries:
                for part in entry.parent.parts:
                    if not public_modname_from_folder(part):
                        print(f"skip {entry} due to {part} is not a public package name")
                        break
                else:
                    if entry.stem.startswith('bench_') or entry.stem.endswith('_bench'):
                        bench_files[entry] = None

        elif p.is_file():
            bench_files[p] = None

        else:
            raise ValueError(
                f"Path '{p}' is neither a plain file nor a directory."
            )

    return list(bench_files.keys())


def cli():

    arguments = docopt(__doc__, version=minghu6.__version__)

    # print(arguments)

    if arguments['--classic-runner']:
        runner = classic_run_a_benchmark
    else:
        runner = run_a_benchmark

    casenames = arguments['--case-name']

    if arguments['-m']:
        modname = arguments['<module-name>']

        try:
            m = import_module(modname)
        except ModuleNotFoundError as ex:
            if ex.name and (
                ex.name == modname or modname.startswith(f"{ex.name}.")
            ):
                exit(f"error: no module named `{modname}`")

            raise
        except ImportError as ex:
            exit(f"error: cannot import `{modname}`: {ex}")
        else:
            bench_on_module(m, casenames, runner=runner)
    else:
        if base_dir := arguments['--base-dir']:
            discover_virtual_packages(base_dir)

        try:
            bench_files = collect_bench_files(
                arguments["<bench-path>"], arguments["-r"]
            )
        except (FileNotFoundError, ValueError) as ex:
            exit(f"error: {ex}")

        for bench_file in bench_files:
            m = load_script(bench_file, base_dir)
            bench_on_module(m, casenames, runner=runner)


if __name__ == "__main__":
    cli()
