# -*- coding:utf-8 -*-
"""
################################################################################
Nothing
################################################################################
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setup import __version__ as VERSION

__version__ = VERSION
print(__version__)
