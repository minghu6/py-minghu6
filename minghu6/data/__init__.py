
from functools import singledispatch
from collections.abc import Iterable
from collections import Counter

from public import public


@public
def duplicated[T](input: Iterable[T]) -> list[T]:
    d = Counter(input)

    return [e for e in d if d[e] > 1]


@public
@singledispatch
def trim[T](obj: T) -> T:
    raise NotImplementedError

@trim.register
def _(obj: dict) -> dict:
    """
    >>> trim({1:2, 2: None, 3:4})
    {1: 2, 3: 4}
    """

    return dict([(k, v) for k, v in obj.items() if v is not None])

