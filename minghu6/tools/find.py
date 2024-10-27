# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""Find

Usage:
  find [--path=<start-path>]  [--exec=<exec-program>] [--regex=<regex-match>] [--dry] [-i] <pattern>...

Options:
  pattern                   such as '*.c' '*.py', quote is essential for *nix shell for stop '*' from expanding
  -p --path=<start-path>    find start from startdir(default os.curdir)
  -e --exec=<exec-program>  exec other command by pipe like -exec "xxx %s ", %s:file-name
  -r --regex=<regex-match>  use regex match
  -i                        print stats
  --dry                     dry run

Examples:
  # repair broken filename caused by virus.
  find -p . "*.enfp" -e "echo {} | sed 's/.enfp.*//' | xargs -0 mv {}"
"""
import os

import minghu6
import minghu6.cmd as cmd
from docopt import docopt
from minghu6.etc.find import find


def handle_exec_string(raw_s: str, fn: str) -> str:
    raw_s = raw_s.replace("{}", f'"{fn}"')

    return raw_s


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    if arguments["--path"] is None:
        start_path = os.curdir
    else:
        start_path = arguments["--path"]

    start_path = start_path
    cnt = 0

    for fn in find(
        *arguments["<pattern>"], startdir=start_path, regex_match=arguments["--regex"]
    ):
        cnt += 1

        if arguments["--exec"]:
            if os.path.isfile(fn):
                exec_cmd_completely = handle_exec_string(arguments["--exec"], fn)
                if arguments["--dry"]:
                    print(exec_cmd_completely)
                else:
                    print(fn)
                res = cmd.wait_run(exec_cmd_completely)
                print(res.out + res.err)
        else:
            print(fn)

    if arguments["-i"]:
        print()
        print(f"total: {cnt}")


if __name__ == "__main__":
    cli()
