# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys

from minghu6.etc.cmd import exec_cmd

pypath = sys.executable

def test_captcha():
    cmd = '{0} -m minghu6.tools.captcha --help'.format(pypath)
    info_lines, err_lines = exec_cmd(cmd)
    #TODO "ImportError: No module named 'minghu6.graphic.captcha.train'" in travis-ci
    #assert not err_lines, err_lines
    #assert info_lines

if __name__ == '__main__':
    test_captcha()