# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
time  count the running total time(default `xxx s`)

Usage:
  time <command-to-run> [--unit=<unit>]

Options:
  <command-to-run>  such as `time "python3 -m minghu6.tools.head a.txt"`
  --unit=<unit>     ms, s, min, h

"""
from docopt import docopt

import minghu6
from minghu6.algs.timeme import timeme
from minghu6.etc.cmd import exec_cmd
from minghu6.text.color import color

def main(command, unit='s'):
    with timeme(unit=unit) as t:
        info_lines, err_lines = exec_cmd(command)

    color.print_info('\n'.join(info_lines))
    color.print_err('\n'.join(err_lines))
    color.print_info(t)


def interactive():
    arguments = docopt(__doc__, version=minghu6.__version__)
    #print(arguments)
    if arguments['--unit']:
        unit=arguments['--unit']
    else:
        unit='s'

    main(arguments['<command-to-run>'], unit=unit)

if __name__ == '__main__':
    interactive()
