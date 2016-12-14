# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
About Import function, class
################################################################################
"""
import importlib
from importlib import import_module

from minghu6.etc.cmd import exec_cmd
from minghu6.etc.version import ispython2,ispython3

def check_module(module_name,install_name=''):
    """
    check if the module exist, if not exist try to install by pip
    (you can provide the install name manually)
    :param module_name:
    :param install_name: default equals module name
    :return:
    """
    try:
        import_module(module_name)

    except ImportError:
        print(module_name,'Not Exists')

        pip_name=''
        if ispython3():
            pip_name='pip3'
        elif ispython2():
            pip_name='pip'

        print('Now, try to install through {}'.format(pip_name))

        if install_name in ('',None):
            install_name=module_name

        info_lines, err_lines=exec_cmd('{0} install {1}'.format(pip_name,install_name))
        print(''.join(info_lines))
        if len(err_lines)!=0:
            print(''.join(err_lines))

    else:
        print('installed')

def add_parent_path(plevel=1):
    """
    Solve "Parent module '' not loaded, cannot perform relative import" Issue
    :param plevel:
    :return:
    """
    from minghu6.etc.path import get_pre_path
    import os

    path = get_pre_path(__file__, plevel)

    os.path.join(path)

if __name__ == '__main__':
    check_module('1234','1234')
    #add_parent_path(plevel=3)