# -*- coding:utf-8 -*-
"""
################################################################################
Nothing
################################################################################
"""
import re
import os
import codecs

def find_version():
    here = os.path.abspath(os.path.dirname(__file__))
    there = os.path.join(os.path.dirname(here), 'setup.py')

    version_file = codecs.open(there, 'r').read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)

    else:
        raise RuntimeError("Unable to find version string.")

__version__ = find_version()
