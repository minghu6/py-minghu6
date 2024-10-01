from typing import Iterator

import minghu6


def iterator_same(iter_obj: Iterator, strict=False) -> bool:
    """
    >>> iterator_same(iter([]))
    True
    >>> iterator_same(iter([]))
    True
    >>> iterator_same(iter([]), strict=True)
    Traceback (most recent call last):
        ...
    ValueError
    >>> iterator_same(iter([1, 1, 1]), strict=True)
    True
    >>> iterator_same(iter([1, 2, 1]), strict=True)
    False
    """

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


def iterator_zip_eq(
    obj0: Iterator, obj1: Iterator, *other_objs: Iterator, key=lambda x: x, strict=False
) -> bool:
    """ """

    try:
        return all(
            map(
                lambda x: iterator_same(iter(x), strict=strict),
                zip(obj0, obj1, *other_objs, strict=strict),
            )
        )
    except ValueError:
        return False


if __name__ == "__main__":
    import doctest

    doctest.testmod(m=minghu6)
