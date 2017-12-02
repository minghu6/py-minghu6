# -*- coding:utf-8 -*-


def chain_apply(funcs, var):
    """apply func from funcs[0] to funcs[-1]"""
    for func in funcs:
        var = func(var)

    return var
