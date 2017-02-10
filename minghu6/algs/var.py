#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#python3

__all__ = ['isset',
           'isiterable',
           'get_typename_str',
           'allis',
           'each_same',
           'isnum_str']


def isset(var_str):

    """
    Not Need,we should use var_str in dir() not call this func 
    """
    pass
    #return var_str in dir()

def isiterable(obj, but_str_bytes=True):
    """
    :param obj:
    :param but_str: most of time, we don't need str
    :return:
    """
    from collections import Iterable
    if but_str_bytes and isinstance(obj, (str, bytes, bytearray)):
        return False
    else:
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

def each_same(iterableObj, *other_iterableObjs, key=lambda x:x):
    """
    have side-effect for generator!
    :param iterableObj1:
    :param iterableObj2:
    :return:
    """
    import types
    if isinstance(iterableObj, types.GeneratorType): #Warning: the generator will be ruined
        iterableObj = [item for item in iterableObj]

    if len(other_iterableObjs) == 0:# same self
        if len(iterableObj) <= 1:
            return True

        sample = iterableObj[0]
        for item in iterableObj:
            if key(item) != key(sample):
                return False

        return True
    else:
        for every_other_iterable in other_iterableObjs:
            if isinstance(every_other_iterable, types.GeneratorType):
                every_other_iterable = [item for item in every_other_iterable]

            if len(iterableObj) != len(every_other_iterable):
                return False
            for item1, item2 in zip(iterableObj, every_other_iterable):
                if key(item1) != key(item2):
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













