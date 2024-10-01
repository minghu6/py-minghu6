"""Introspect

Usage:
  introspect ( minghu6_home | version | tools )

Options:
"""

import minghu6
from minghu6.tools import get_module_names


def cli():
    from docopt import docopt

    arguments = docopt(__doc__, version=minghu6.__version__)

    if arguments["minghu6_home"]:
        print(minghu6.MINGHU_HOME)
    elif arguments["version"]:
        print(minghu6.__version__)
    elif arguments['tools']:
        print(' '.join(get_module_names()))


if __name__ == "__main__":
    cli()
