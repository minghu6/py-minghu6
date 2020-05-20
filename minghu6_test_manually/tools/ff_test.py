# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import sys

from minghu6.algs.operator import getone
from minghu6.etc.cmd import exec_cmd

pypath = sys.executable


def test_ff():
    cmd = '{0} -m minghu6.tools.ff --help'.format(pypath)
    info_lines, err_lines = exec_cmd(cmd)
    assert getone(err_lines, 0, 'failed') == ''
    assert info_lines


if __name__ == '__main__':
    test_ff()
