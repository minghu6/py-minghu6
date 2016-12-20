# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys
from .constants import *

from minghu6.text.color import color
def history(args):
    with open(HISTORY_PATH, 'r') as history_file:
        lines = history_file.readlines()
        limit = len(lines)
        if len(args) > 0:
            limit = int(args[0])
        start = len(lines) - limit
        for line_num, line in enumerate(lines):
            if line_num >= start:
                color.printBlank('{0} {1}'.format(line_num + 1, line))


    return SHELL_STATUS_RUN
