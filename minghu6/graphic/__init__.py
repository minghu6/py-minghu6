#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
using: about graphic 2D and 3D
need: numpy matplotlib (pip3 install matplotlib)
################################################################################
"""
from minghu6.etc.cmd import exec_cmd
from minghu6.etc.version import ispython2,ispython3

if ispython3():
    pip_name='pip3'
elif ispython2():
    pip_name='pip'
else:
    raise Exception('can not find cmd python')

try:
    import numpy
except ImportError:
    s=exec_cmd([pip_name,'install','numpy'])[0]
    print(''.join(s))

try:
    import matplotlib
except ImportError:
    s=exec_cmd([pip_name,'install','numpy'])[0]
    print(''.join(s))

try:
    import PIL
except ImportError:
    s=exec_cmd([pip_name,'install','pillow'])[0]
    print(''.join(s))

