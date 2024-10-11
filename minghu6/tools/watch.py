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
from minghu6.etc.cmd import exec_cmd
from color import color

from minghu6.test.bench import Watch


def main(command):
    with Watch() as w:
        info_lines, err_lines = exec_cmd(command)

    color.print_info("\n".join(info_lines))
    color.print_err("\n".join(err_lines))
    color.print_info(w)


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    main(arguments["<command-to-run>"])


if __name__ == "__main__":
    cli()
