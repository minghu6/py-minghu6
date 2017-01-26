# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys
import os

from minghu6.etc.path import get_pre_path
pypath = sys.executable

from minghu6.tools import add_pypath

def test_add_pypath():
    common_path = get_pre_path(__file__, 3)
    target_path = os.path.join(common_path, 'minghu6', 'tools', 'add_pypath.py')
    cmd = '{0} {1} --help'.format(pypath, target_path)
    assert os.system(cmd) == 0

if __name__ == '__main__':
    test_add_pypath()