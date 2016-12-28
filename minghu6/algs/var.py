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

def get_typename_str(Object):
    return getattr(Object, '__name__') if hasattr(Object, '__name__') else getattr(Object, '__class__')


def allis(iterableObj, type):
    """
    i.e.
    res=allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))
    #True

    :param iteras:
    :param type:
    :return:
    """
    for itera in iterableObj:
        if not isinstance(itera, type):
            return False
    return True

def allequal(iterableObj1, iterableObj2):
    """

    :param iterableObj1:
    :param iterableObj2:
    :return:
    """
    import types
    if isinstance(iterableObj1, types.GeneratorType):
        iterableObj1 = [item for item in iterableObj1]

    if isinstance(iterableObj2, types.GeneratorType):
        iterableObj2 = [item for item in iterableObj2]


    if len(iterableObj1) != len(iterableObj2):
        return False

    for item1, item2 in zip(iterableObj1, iterableObj2):
        if item1 != item2:
            return False

    return True

def isnum_str(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


if __name__=='__main__':

    res=allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable('abc'))













