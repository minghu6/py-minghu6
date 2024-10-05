from collections.abc import Iterable, Iterator
from collections import Counter


def duplicated(input: Iterable) -> list:
    d = Counter(input)

    return [e for e in d if d[e] > 1]


# input is ordered
def dedup(input: Iterable) -> list:
    if not isinstance(input, Iterator):
        input = iter(input)

    new = []

    try:
        prev = next(input)
    except StopIteration:
        return new
    else:
        new.append(prev)

    for e in input:
        if e != prev:
            new.append(e)
        prev = e

    return new
