# -*- coding:utf-8 -*-


from collections.abc import Callable, Iterable
from functools import partial
from itertools import chain
from typing import Any

from public import public

from minghu6.itertools import skip, nth


type Functor = Callable[[Iterable], Iterable]


@public
def chain_apply(*funcs):
    """apply func from funcs[0] to funcs[-1]"""

    var = funcs[-1]

    for func in funcs[:-1][::-1]:
        var = func(var)

    return var


builtin_map = map
builtin_filter = filter
itertools_chain = chain
_skip = skip
_nth = nth


@public
def map(f):
    return partial(builtin_map, f)


@public
def filter[T](f: Callable[[Iterable[T]], bool]):
    return partial(builtin_filter, f)


@public
def chain(snd_iterabel: Iterable):
    return xargs(itertools_chain, snd_iterabel)


@public
def skip(n: int):
    return partial(_skip, n=n)


@public
def nth(n: int):
    return partial(_nth, n=n)


@public
def xargs(f: Functor, snd_iterable: Iterable) -> Functor:
    def inner(fst_iterable: Iterable) -> Iterable:
        return f(fst_iterable, snd_iterable)

    return inner
