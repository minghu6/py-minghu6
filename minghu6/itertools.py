from collections.abc import Generator, Iterable,Sequence
from public import public


@public
def same(items: Iterable, strict=False) -> bool:
    """
    Iterable is superclass of Iterator,
    iter(Iterator) = itself

    >>> same([])
    True
    >>> same(iter([]))
    True
    >>> same(iter([]), strict=True)
    Traceback (most recent call last):
        ...
    ValueError
    >>> same(iter([1, 1, 1]), strict=True)
    True
    >>> same(iter([1, 2, 1]), strict=True)
    False
    """

    iter_obj = iter(items)

    stopped = False

    try:
        first = next(iter_obj)

    except StopIteration:
        stopped = True

    finally:
        if stopped:
            if strict:
                raise ValueError

            return True

    try:
        second = next(iter_obj)
    except StopIteration:
        stopped = True

    finally:
        if stopped:
            if strict:
                raise ValueError

            return True

    return first == second and all(map(lambda x: x == first, iter_obj))

@public
def zip_eq(
    obj0: Iterable, obj1: Iterable, *other_objs: Iterable, key=lambda x: x, strict=False
) -> bool:
    """ """

    try:
        return all(
            map(
                lambda x: same(x, strict=strict),
                zip(obj0, obj1, *other_objs, strict=strict),
            )
        )
    except ValueError:
        return False

@public
def split_ind(s: Sequence, ind: int):
    return (s[:ind], s[ind:])

@public
def split[T](s: Sequence[T], v: T):
    for i, sv in enumerate(s):
        if sv == v:
            return (s[:i], s[i + 1 :])
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
