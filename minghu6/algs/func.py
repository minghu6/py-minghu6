# -*- coding:utf-8 -*-

from collections import Iterable


def chain_apply(funcs, var):
    """apply func from funcs[0] to funcs[-1]"""
    for func in funcs:
        var = func(var)

    return var


def flatten(items, class_type=None):
    """Yield items from any nested iterable; see REF."""
    for x in items:
        if class_type is not None and not isinstance(x, class_type):
            yield from flatten(x)
        elif isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x
