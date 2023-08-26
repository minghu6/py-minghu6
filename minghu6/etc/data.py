from typing import Iterable, List, Iterator
from collections import Counter
# from itertools import chain, pairwise


def duplicated(input: Iterable) -> List:
    d = Counter(input)

    return [e for e in d if d[e]>1]


# input is ordered
def dedup(input: Iterable) -> List:
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
