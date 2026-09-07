"""DocTest

Usage:
    doctest <module-name>... [--obj-name=<oname>]... [--recursive] [--strict] [--verbose]...

Options:
    -o --obj-name=<oname>    specfic obj to run its doc
    -r --recursive           run doctest on <module-name> recursive
    --strict                 use strict mode
    --verbose                print details
"""

from docopt import docopt


import minghu6
from minghu6.test.doctest import run_doctest


def cli():

    arguments = docopt(__doc__, version=minghu6.__version__)

    for m in arguments["<module-name>"]:
        run_doctest(
            m,
            onames=arguments["--obj-name"],
            strict=arguments["--strict"],
            recursive=arguments["--recursive"],
            verbose=arguments["--verbose"],
        )


if __name__ == "__main__":
    cli()
