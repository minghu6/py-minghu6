# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import sys

from minghu6.algs.operator import getitem
from minghu6.etc.cmd import exec_cmd

pypath = sys.executable


def test_ffmpeg_fix():
    cmd = '{0} -m minghu6.tools.ffmpeg_fix --help'.format(pypath)
    info_lines, err_lines = exec_cmd(cmd)
    assert getitem(err_lines, 0, 'failed') == ''
    assert info_lines


if __name__ == '__main__':
    test_ffmpeg_fix()
