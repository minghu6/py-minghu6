# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys

from minghu6.etc.cmd import exec_cmd
from minghu6.tools import youtube

pypath = sys.executable

def test_youtube():
    cmd = '{0} -m minghu6.tools.youtube --help'.format(pypath)
    info_lines, err_lines = exec_cmd(cmd)
    assert not err_lines
    assert info_lines


if __name__ == '__main__':
    test_youtube()