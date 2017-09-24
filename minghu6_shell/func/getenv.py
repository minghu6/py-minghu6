# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from color import color

from .constants import *


def getenv(args):
    if len(args) > 0:
        color.print_info(os.getenv(args[0]))

    return SHELL_STATUS_RUN
