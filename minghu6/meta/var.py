# -*- coding:utf-8 -*-

import sys

import re
import collections


if sys.hexversion >= 0x030A00F0:
    from collections.abc import *
else:
    from collections import *


def isiterable(obj, but_str_bytes=True):
    if but_str_bytes and isinstance(obj, (str, bytes, bytearray)):
        return False
    else:
        return isinstance(obj, Iterable)


def get_type_str(Object) -> str:
    return (
        getattr(Object, "__name__")
        if hasattr(Object, "__name__")
        else getattr(Object, "__class__")
    )


def istypeof(iterable_obj, type):
    """
    >>> allis(['abcd', ['a', 'b', 'c'], 'fff'], (str, list))
    True
    """
    for item in iterable_obj:
        if not isinstance(item, type):
            return False
    return True


def isnumstr(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def find_attrs(obj, pattern):
    return [
        getattr(obj, attr_name)
        for attr_name in dir(obj)
        if re.match(pattern, attr_name)
    ]


def namedtuple(*args, **kwargs):
    result = collections.namedtuple(*args, **kwargs)

    def to_dict(self):
        return dict([(field, getattr(self, field)) for field in self._fields])

    result.to_dict = to_dict

    return result



if __name__ == "__main__":
    res = istypeof(["abcd", ["a", "b", "c"], "fff"], (str, list))

    print(res)

    print(isiterable(None))
    print(isiterable("abc"))
