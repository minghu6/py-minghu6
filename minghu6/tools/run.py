"""Run
Run a python module with `-m module_absolute_path`

Usage:
    run <module-name>

Options:

"""

from importlib import import_module
from docopt import docopt

import minghu6
from minghu6.test.bench import bench_on_module


def cli():

    arguments = docopt(__doc__, version=minghu6.__version__)

    # print(arguments)
    # for pypath in arguments["--add-path"]:
    #     sys.path.append(pypath)

    # for m in arguments["<module-name>"]:
    #     run_doctest(
    #         m,
    #         onames=arguments["--obj-name"],
    #         strict=arguments["--strict"],
    #         recursive=arguments["--recursive"],
    #         verbose=arguments["--verbose"],
    #     )

    try:
        m = import_module(arguments['<module-name>'])
    except ImportError:
        print("No module found")
    else:
        
        print()


if __name__ == "__main__":
    cli()
