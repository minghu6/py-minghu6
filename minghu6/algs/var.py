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


def unify_to_iterable(var):
    if isiterable(var):
        return var

    return [var]


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


from types import MethodType


class CustomMeta(type):
    def __new__(cls, name, bases, attrs):
        if 'extra_attrs' not in attrs:
            attrs['extra_attrs'] = {}

        return type.__new__(cls, name, bases, attrs)


class CustomStr(object, metaclass=CustomMeta):

    @staticmethod
    def _wrap_callable(self, method):

        def newmethod(self, *args, **kwargs):
            result = method(*args, **kwargs)
            if isinstance(result, str):
                result = CustomStr(result)

            return result

        return MethodType(newmethod, self)

    def _wrap_replace_s(method):
        def newmethod(self, *args, **kwargs):
            return getattr(self._s, method.__name__)(*args, **kwargs)

        return newmethod

    def __init__(self, *args, **kwargs):
        self._s = str(*args, **kwargs)

        newattrs = {}
        for attrname in dir(str):
            if not attrname.startswith('__'):
                attrvalue = getattr(self._s, attrname)
                if callable(attrvalue):
                    setattr(self, attrname, CustomStr._wrap_callable(self, attrvalue))
                    # print(attrname)

        # print(self.swapcase)

    @_wrap_replace_s
    def __str__(self):
        pass

    @_wrap_replace_s
    def __repr__(self):
        pass


if __name__ == '__main__':
    res = allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable('abc'))
