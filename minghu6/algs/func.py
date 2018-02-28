# -*- coding:utf-8 -*-

from collections import Iterable


def chain_apply(funcs, var):
    """apply func from funcs[0] to funcs[-1]"""
    for func in funcs:
        var = func(var)

    return var


def flatten(items):
    """Yield items from any nested iterable; see REF."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x
