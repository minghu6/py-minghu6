# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from .constants import *

def cd(args):
    if len(args) > 0:
        os.chdir((args[0]))
    else:
        os.chdir(os.getenv('HOME'))
    return SHELL_STATUS_RUN
