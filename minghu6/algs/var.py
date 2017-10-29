#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# python3

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
    # return var_str in dir()


def isiterable(obj, but_str_bytes=True):
    """
    :param obj:
    :param but_str_bytes: most of time, we don't need str and bytes
    :return:
    """
    from collections import Iterable
    if but_str_bytes and isinstance(obj, (str, bytes, bytearray)):
        return False
    else:
        return isinstance(obj, Iterable)


def get_typename_str(Object):
    return getattr(Object, '__name__') if hasattr(Object, '__name__') else getattr(Object, '__class__')


def allis(iterable_obj, type):
    """
    i.e.
    res=allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))
    #True

    :param iterable_obj:
    :param type:
    :return:
    """
    for itera in iterable_obj:
        if not isinstance(itera, type):
            return False
    return True


def each_same(iterable_obj, *other_iterable_objs, key=lambda x: x):
    """
    have side-effect for generator!
    :param iterable_obj1:
    :param iterable_obj2:
    :return:
    """
    import types
    if isinstance(iterable_obj, types.GeneratorType):  # Warning: the generator will be ruined
        iterable_obj = [item for item in iterable_obj]

    if len(other_iterable_objs) == 0:  # same self
        if len(iterable_obj) <= 1:
            return True

        sample = iterable_obj[0]
        for item in iterable_obj:
            if key(item) != key(sample):
                return False

        return True
    else:
        for every_other_iterable in other_iterable_objs:
            if isinstance(every_other_iterable, types.GeneratorType):
                every_other_iterable = [item for item in every_other_iterable]

            if len(iterable_obj) != len(every_other_iterable):
                return False
            for item1, item2 in zip(iterable_obj, every_other_iterable):
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


if __name__ == '__main__':
    res = allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable('abc'))
