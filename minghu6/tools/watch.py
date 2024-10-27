# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
time  count the running total time(default `xxx s`)

Usage:
  time <command-to-run>

Options:
  <command-to-run>  such as `time "python3 -m minghu6.tools.head a.txt"`

"""
import minghu6
from docopt import docopt
from minghu6.cmd import wait_run
from color import color

from minghu6.test.profile import Watch


def main(command):
    with Watch() as w:
        res = wait_run(command)

    color.print_info(res.out)
    color.print_err(res.err)
    color.print_info(w)


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    main(arguments["<command-to-run>"])


if __name__ == "__main__":
    cli()
