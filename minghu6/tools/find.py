# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""Find

Usage:
  find [--path=<start-path>] <pattern>... [--exec=<exec-program>] [--regex=<regex-match>]
                                          [--debug=<debug-mode>]

Options:
  pattern                   such as *.c *.py
  -p --path=<start-path>    find start from startdir(default os.curdir)
  -e --exec=<exec-program>  exec other command by pipe like -exec "xxx %s ", %s:file-name
  -r --regex=<regex-match>  use regex match
  -d --debug=<debug-mode>   turn on debug mode

"""
import os

import minghu6
import minghu6.etc.cmd as cmd
from docopt import docopt
from minghu6.etc.find import find
from pprint import pprint


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    if arguments['--path'] is None:
        start_path = os.curdir
    else:
        start_path = arguments['--path']

    for fn in find(arguments['<pattern>'], start_path,
                   regex_match=arguments['--regex']):
        if arguments['--exec'] is not None:
            if os.path.isfile(fn):
                pprint(fn)
                # print(arguments['--exec'])
                exec_cmd_completely = arguments['--exec'] % fn

                if arguments['--debug']:
                    pprint(exec_cmd_completely)
                info, err = cmd.exec_cmd(exec_cmd_completely)

                print('\n'.join(info), '\n'.join(err))
        else:
            pprint(fn)


if __name__ == '__main__':
    cli()
