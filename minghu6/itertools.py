from collections.abc import Generator, Iterable, Sequence
from itertools import islice
from public import public



@public
def split[T](s: Sequence[T], v: T):
    for i, sv in enumerate(s):
        if sv == v:
            return (s[:i], s[i + 1:])
    return ([], s)


@public
def flattenall(items, class_type=None, include_str=False) -> Generator:
    """Yield items from any nested iterable

    >>> list(flattenall([1, [2, [3]], 4, [[[5]]]]))
    [1, 2, 3, 4, 5]
    """
    for x in items:
        if class_type is not None and not isinstance(x, class_type):
            yield from flattenall(x)
        elif isinstance(x, Iterable):
            if not include_str and isinstance(x, (str, bytes)):
                yield x
            else:
                yield from flattenall(x)
        else:
            yield x


@public
def flatten[T](items: Iterable[T]) -> Generator[T, None, None]:
    """ flatten strict one level, use `flattenall` for loose version.
    >>> list(flatten([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    >>> list(flatten([[1, 2], [3, [4]]]))
    [1, 2, 3, [4]]
    >>> list(flatten([1, 2, [3, 4]]))
    Traceback (most recent call last):
        ...
    TypeError: 'int' object is not iterable
    """
    for item in items:
        yield from item


@public
def nest[T](items: Iterable[T]) -> Iterable[T]:
    """
    >>> list(nest([1, 2, 3, 4]))
    [[1], [2], [3], [4]]
    >>> list(flatten(nest([1, 2, 3, 4])))
    [1, 2, 3, 4]
    """

    return map(
        lambda item: [item],
        items
    )


@public
def skip[T](iterable: Iterable[T], n: int) -> Iterable[T]:
    """
    >>> list(skip([1, 2, 3], 0))
    [1, 2, 3]
    >>> list(skip([1, 2, 3], 2))
    [3]
    >>> list(skip([1, 2, 3], 3))
    []
    """

    return islice(iterable, n, None)


@public
def nth[T](iterable: Iterable[T], n: int) -> T:
    """
    :n: base 0

    >>> nth([1, 2, 3], 0)
    1
    >>> nth([1, 2, 3], 2)
    3
    >>> nth([1, 2, 3], 3)
    Traceback (most recent call last):
        ...
    StopIteration
    """

    return next(skip(iterable, n))

