#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# python3

import functools

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


def _wrap_replace_s(method):
    @functools.wraps(method)
    def newmethod(self, *args, **kwargs):
        return getattr(self._s, method.__name__)(*args, **kwargs)

    return newmethod


# def custom_str(*args, **kwargs):
#     pass

class CustomStrBytesCommon(object):

    @property
    def _custom_class(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        self._s = self._custom_class(*args, **kwargs)
        allowed_magic_method = ['__str__',
                                '__repr',
                                '__add__',
                                '__contains__',
                                '__format__',
                                '__iter__',
                                '__len__']

        def _wrap_callable(self, method):
    
            def newmethod(self, *args, **kwargs):
                result = method(*args, **kwargs)
                if isinstance(result, str):
                    result = CustomStr(result)
                    setattr(result, 'extra_attrs', self.extra_attrs)
                elif isinstance(result, bytes):
                    result = CustomBytes(result)
                    setattr(result, 'extra_attrs', self.extra_attrs)

                return result
    
            return MethodType(newmethod, self)

        for attrname in dir(self._custom_class):
            if not attrname.startswith('__') or attrname in allowed_magic_method:
                attrvalue = getattr(self._s, attrname)
                if callable(attrvalue):
                    setattr(self, attrname, _wrap_callable(self, attrvalue))
        
        if len(args) == 0 or not hasattr(args[0], 'extra_attrs'):
            self.extra_attrs = {}

    def __eq__(self, s):
        if self._s != s:
            return False
        
        if self.extra_attrs != getattr(s, 'extra_attrs', {}):
            return False

        return True

    def __ne__(self, s):
        return not self.__eq__(s)

    # TODO
    # '__reduce__',
    # '__reduce_ex__',


class CustomBytes(CustomStrBytesCommon, bytes):
    @property
    def _custom_class(self):
        return bytes


class CustomStr(CustomStrBytesCommon, str):
    @property
    def _custom_class(self):
        return str


if __name__ == '__main__':
    res = allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable('abc'))
