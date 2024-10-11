"""Bench

running benchmarks of a module.

Usage:
  bench <module-name> [<case-name>]... [--classic-runner]

Options:
  --classic-runner  use Python `Timer::autorange` as benche_runner
"""

from importlib import import_module
from docopt import docopt

import minghu6
from minghu6.test.bench import (
    Watch,
    bench_on_module,
    classic_run_a_benchmark,
    run_a_benchmark
)


def cli():

    arguments = docopt(__doc__, version=minghu6.__version__)

    # print(arguments)

    try:
        m = import_module(arguments['<module-name>'])

    except ImportError:
        print("No module found")

    else:
        if arguments['--classic-runner']:
            runner = classic_run_a_benchmark
        else:
            runner = run_a_benchmark

        with Watch() as w:
            bench_on_module(
                m,
                casenames=arguments['<case-name>'],
                runner=runner
            )

        print()
        print(f"spent {w.secs:.2f} secs")


if __name__ == "__main__":
    cli()
