"""Introspect

Usage:
  introspect ( minghu6_home | version | tools )
  introspect modules [--pkg=<pkg>] [-P]

Options:
  -p --pkg=<pkg>  spec package name [default: .]
  -P              print with prefix name
"""

import pkgutil

import minghu6
from minghu6.etc.importer import list_submodule_names
from minghu6.itertools import flatten
from minghu6.tools import find_tool_module_names


def cli():
    from docopt import docopt

    arguments = docopt(__doc__, version=minghu6.__version__)

    if arguments["minghu6_home"]:
        print(minghu6.MINGHU_HOME)
    elif arguments["version"]:
        print(minghu6.__version__)
    elif arguments["tools"]:
        print(" ".join(find_tool_module_names()))
    elif arguments["modules"]:
        m: str = arguments["--pkg"]

        if m.endswith("."):
            m = m[:-1]

        if not m:
            print(" ".join(map(lambda m: m.name, pkgutil.iter_modules())))
        else:
            try:
                ps, ms = list_submodule_names(m)
            except ImportError:
                print("")
            else:
                names = ps + ms

                if arguments["-P"]:
                    names = map(lambda x: f"{m}.{x}", names)

                print(" ".join(names))


if __name__ == "__main__":
    cli()
