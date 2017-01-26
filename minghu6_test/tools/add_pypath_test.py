# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys
import os
from minghu6.etc.cmd import exec_cmd

pypath = sys.executable

def test_add_pypath():
    cmd = '{0} -m minghu6.tools.add_pypath --help'.format(pypath)
    print(pypath)
    assert os.system(cmd) == 0

if __name__ == '__main__':
    test_add_pypath()