#! /usr/bin/env python3
# -*- Coding:utf-8 -*-

"""
################################################################################
run to install the minghu6 python-package;
be independent on minghu6's other content.
################################################################################
"""

import os
import sys

def make_pth_file(abs_pac_target_path=str()):

    abs_curdir=os.path.abspath(os.path.curdir)
    abs_par_curdir=os.path.split(abs_curdir)[0]

    if abs_pac_target_path.strip() in (str(),'.'):
        abs_pac_target_path=abs_par_curdir

    if iswin() and sys.version_info.major==2:
        raise Exception('\n\n\tIt\'s python2 not python3\n'
                        '\tPlease run in python3\n'
                        '\tBecause minghu6 pacage is mostly based on python3\n')

    pth_dir=''
    if iswin():
        pth_dir=os.path.split(sys.executable)[0]
    elif islinux():
        pth_dir=get_target_path()

    pth_file=os.path.join(pth_dir,'minghu6.pth')
    print(abs_pac_target_path,pth_file)
    with open(pth_file,'a') as file:
        file.write('{0:s}\n'.format(abs_pac_target_path))

import platform

def islinux():
    return platform.platform().upper().startswith('LINUX')
def iswin():
    return platform.platform().upper().startswith('WIN')
def get_target_path():
    if islinux():
        for path in sys.path:
            if os.path.basename(path)=='dist-packages':
                return path


if __name__=='__main__':
    if len(sys.argv)>1:
        make_pth_file(sys.argv[1])
        #print(sys.argv[1])
        #os.system('pause')
    else:
        make_pth_file()
