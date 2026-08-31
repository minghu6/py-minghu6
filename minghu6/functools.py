# -*- coding:utf-8 -*-


from collections.abc import Callable, Iterable
from functools import partial
from itertools import chain

from exports import export

from minghu6.itertools import skip, nth


type Functor = Callable[[Iterable], Iterable]


@export
def chain_apply(*funcs: Functor | Iterable) -> Iterable:
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


@export
def map(f):
    return partial(builtin_map, f)


@export
def filter[T](f: Callable[[Iterable[T]], bool]):
    return partial(builtin_filter, f)


@export
def chain(snd_iterabel: Iterable):
    return xargs(itertools_chain, snd_iterabel)


@export
def skip(n: int):
    return partial(_skip, n=n)


@export
def nth(n: int):
    return partial(_nth, n=n)


@export
def xargs(f: Functor, snd_iterable: Iterable) -> Functor:
    def inner(fst_iterable: Iterable) -> Iterable:
        return f(fst_iterable, snd_iterable)

    return inner
