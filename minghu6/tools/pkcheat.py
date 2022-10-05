# -*- coding:utf-8 -*-


"""pkcheat
Pokemon cheats converter

Usage:
  pkcheat <patten> [-o=output]

Options:
  <output>   output file

"""

import json
from docopt import docopt

import minghu6


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    path = arguments['<patten>']

    obj = json.load(open(path))
    aiwulist = obj.get('aiWuCheatList')


if __name__ == '__main__':
    cli()
