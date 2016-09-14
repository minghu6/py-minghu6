# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os
from importlib import import_module
from minghu6.etc.find import find

def main():
    curpath = os.path.dirname(__file__)
    #print(curpath)
    def filter_module(module_name):
        if module_name.find('__init__') != -1:
            return False
        elif module_name.find('unitest') != -1:
            return False

        else:
            return True


    for i, fn in enumerate(find('*.py', curpath)):

        module_name =fn[len(curpath)+1:-3]
        if filter_module(module_name):
            m = import_module('minghu6.tools.'+module_name)
            print(i+1, module_name, m.__doc__)


if __name__ == '__main__':
    main()