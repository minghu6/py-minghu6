#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
################################################################################
About Path(File,Directory,Atty,Link etc)
################################################################################
"""

import os,sys

def get_pre_dir(path):
    '''
    get one level before path
    '''
    #print(path)
    path = os.path.abspath(path)
    return os.path.split(path)[0]

def get_cwd_preDir(n):
    """
    equal to get_cwd_pres_dir
    :param n:
    :return:
    """
    return get_cwd_pres_dir(n)

def get_cwd_pres_dir(n):
    '''
    get n level before cwd 's dir
    '''
    path = get_parent_path(path=os.getcwd(), plevel=n)

    return path

def get_parent_path(path, plevel = 1):

    for i in range(plevel):
        path=get_pre_dir(path)

    return path
def add_parent_path(path, plevel = 1):
    path = get_parent_path(path, plevel)
    os.path.join(path)

def isempty_file(fn):
    with open(fn,'rb') as f:
        length=len(f.read(1))
    return length==0

def isempty_dir(fn):
    return os.listdir(fn).__len__()==0


if __name__ == '__main__':

    path = get_cwd_pres_dir(n=3)
    print(path)

    path = get_parent_path(path = __file__, plevel=19)
    print(path)


