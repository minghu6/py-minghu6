from collections.abc import Callable, Iterable
from functools import partial, reduce
from itertools import chain as legacy_chain

from exports import export

from minghu6.itertools import skip as legacy_skip, nth as legacy_nth


type Functor = Callable[[Iterable], Iterable]


@export
def compose(*funcs: Functor | Iterable) -> Iterable:
    """Like Haskell composition operator `.`, functions are applied from 
    right to left, the final argument is the initial value.
    """

    if len(funcs) < 2:
        raise TypeError("compose() requires at least 2 arguments")

    *funcs, init = funcs

    return reduce(lambda acc, f: f(acc), reversed(funcs), init)


@export
def flow(var: Iterable, *funcs: Functor) -> Iterable:
    """Like Haskell left-to-right composition `>>>`, functions are applied from 
    left to right, the first argument is the initial value.
    """

    for func in funcs:
        var = func(var)

    return var


@export
def fmap(f):
    return partial(map, f)


@export
def keep[T](f: Callable[[Iterable[T]], bool]):
    return partial(filter, f)


@export
def chain(snd_iterabel: Iterable):
    return xargs(legacy_chain, snd_iterabel)


@export
def skip(n: int):
    return partial(legacy_skip, n=n)


@export
def nth(n: int):
    return partial(legacy_nth, n=n)


@export
def xargs(f: Functor, snd_iterable: Iterable) -> Functor:
    def inner(fst_iterable: Iterable) -> Iterable:
        return f(fst_iterable, snd_iterable)

    return inner
