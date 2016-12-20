# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from .constants import *

from minghu6.text.color import color
def getenv(args):
    if len(args) > 0:
        color.print_info(os.getenv(args[0]))

    return SHELL_STATUS_RUN