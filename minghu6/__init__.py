# -*- coding:utf-8 -*-
"""
################################################################################
Nothing
################################################################################
"""
from os.path import abspath, dirname, join

import hy



__version__ = '1.6.1'

MINGHU_HOME = abspath(dirname(__file__))
RESOURCES_HOME = join(dirname(MINGHU_HOME), 'resources')
TEMPLATES_HOME = join(RESOURCES_HOME, 'templates')
