# -*- coding:utf-8 -*-

from collections.abc import Iterable


def chain_apply(funcs, var):
    """apply func from funcs[0] to funcs[-1]"""
    for func in funcs:
        var = func(var)

    return var


def flatten(items, class_type=None, include_str=False):
    """Yield items from any nested iterable; see REF."""
    for x in items:
        if class_type is not None and not isinstance(x, class_type):
            yield from flatten(x)
        elif isinstance(x, Iterable):
            if not include_str and isinstance(x, (str, bytes)):
                yield x
            else:
                yield from flatten(x)
        else:
            yield x


def split_ind(S, ind):
    return (S[:ind], S[ind:])


def split(S, v):
    for i, Sv in enumerate(S):
        if Sv == v:
            return (S[:i], S[i + 1:])
    return ([], S)
