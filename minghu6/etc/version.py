#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import re
import platform

def iswin():
    return platform.platform().upper().startswith('WIN')

def islinux():
    return platform.platform().upper().startswith('LINUX')

def ispython2():
    return sys.version_info.major==2

def ispython3():
    return sys.version_info.major==3

def get_pythonName_in_shell():
    '''
    WARNING: This way will  assumn very mush time(two or three seconds maybe) !!!
    #we assumn that python is in environment variables#
    :return: list of str such as ['python','python3','python3.4']
    '''
    def __python_find():
        """
        Dynamic find the python form can be used
        python
        python3
        python3.1-python3.7
        """
        py_ver=list()

        py='python'
        if os.system(py+' --version')==0:#return 0 for ok,1 for error(confusing)
            py_ver.append(py)

        py3='python3'
        if os.system(py3+' --version')==0:
            py_ver.append(py3)
        for i in range(7):
            one=py3+'.'+str(i+1)
            if os.system(one+' --version')==0:
                py_ver.append(one)

        return py_ver

    __python_find()

def is_strPython():

    py='python'
    return os.system(py+' --version')==0

def is_strPython3():
    py='python3'
    return os.system(py+' --version')==0


if __name__=='__main__':
    print(os.curdir)
