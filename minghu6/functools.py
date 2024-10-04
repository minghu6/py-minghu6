# -*- coding:utf-8 -*-


from functools import partial


def chain_apply(*funcs):
    """apply func from funcs[0] to funcs[-1]"""

    var = funcs[-1]

    for func in funcs[:-1][::-1]:
        var = func(var)

    return var


builtin_map = map
builtin_filter = filter

map = lambda f: partial(builtin_map, f)
filter = lambda f: partial(builtin_filter, f)
