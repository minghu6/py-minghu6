"""Bench
Usage:
    bench <module-name> [<case-name>]...

Options:

"""

from importlib import import_module
from docopt import docopt

import minghu6
from minghu6.test.bench import bench_on_module


def cli():

    arguments = docopt(__doc__, version=minghu6.__version__)

    # print(arguments)

    try:
        m = import_module(arguments['<module-name>'])
    except ImportError:
        print("No module found")
    else:
        bench_on_module(m, casenames=arguments["<case-name>"])
        print()


if __name__ == "__main__":
    cli()
