#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#python3


def isset(var_str):

    """
    Not Need,we should use var_str in dir() not call this func 
    """
    pass
    #return var_str in dir()

def isiterable(obj):
    from collections import Iterable
    return isinstance(obj, Iterable)


def allis(iteras, type):
    """
    i.e.
    res=allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))
    #True

    :param iteras:
    :param type:
    :return:
    """
    for itera in iteras:
        if not isinstance(itera, type):
            return False
    return True


if __name__=='__main__':

    res=allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable('abc'))













