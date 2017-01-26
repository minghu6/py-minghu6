# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys
import os

from minghu6.etc.cmd import exec_cmd
from minghu6.etc.path import chdir

pypath = sys.executable

def test_add_pypath():
    with chdir(os.path.dirname(__file__)):
        cmd = '{0} ../../minghu6/tools/add_pypath.py --help'.format(pypath)
        info_lines, err_lines = exec_cmd(cmd)

    print(pypath, os.path.dirname(__file__))
    assert not err_lines
    assert info_lines

if __name__ == '__main__':
    test_add_pypath()