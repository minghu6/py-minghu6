#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
################################################################################
About Path(File,Directory,Atty,Link etc)
################################################################################
"""

import os,sys
################################################################################
def get_cwd_preDir(n):
    """
    equal to get_cwd_pres_dir
    :param n:
    :return:
    """
    return get_cwd_pre_dir(n)

def get_cwd_pre_dir(n):
    '''
    get n level before cwd 's dir
    '''
    path = get_pre_path(path=os.getcwd(), plevel=n)

    return path

def get_pre_path(path, plevel = 1):
    def get_parent_dir(path):
        '''
        get one level before path
        '''
        #print(path)
        path = os.path.abspath(path)
        return os.path.split(path)[0]

    for i in range(plevel):
        path=get_parent_dir(path)

    return path

################################################################################
import threading
from contextlib import contextmanager
@contextmanager
def chdir(path):

    with threading.Lock():
        oldpath = os.path.abspath(os.curdir)
        try:

            os.chdir(path)
            yield None

        finally:
            os.chdir(oldpath)



def add_parent_path(path, plevel = 1):
    path = get_pre_path(path, plevel)
    os.path.join(path)

def isempty_file(fn):
    with open(fn,'rb') as f:
        length=len(f.read(1))
    return length==0

def isempty_dir(fn):
    return os.listdir(fn).__len__()==0


def add_postfix(fn, postfix, sep='_'):

    name, ext = os.path.splitext(fn)

    return ''.join([name, sep, postfix, ext])



