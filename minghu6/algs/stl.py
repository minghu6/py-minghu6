# -*- Coding:utf-8 -*-
"""

"""

__all__ = ['lower_bound',
           'upper_bound']


def lower_bound(l, k):
    """
    >>> lower_bound([1, 2, 2, 3, 4], 2)
    1
    >>> lower_bound([1, 2, 2, 3, 4], 5)
    -1

    :param l:
    :param k:
    :return:
    """
    if l[-1] < k:
        return -1

    i = len(l) // 2
    start, end = 0, len(l) - 1
    
    while start < end:
        if l[i] >= k:
            end = i
        else:
            start = i + 1
        
        i = start + (end - start) // 2

    return i


def upper_bound(l, k):
    """
    >>> upper_bound([1, 2, 2, 3, 4], 2)
    3
    >>> upper_bound([1, 2, 2, 3, 4], 5)
    -1

    :param l:
    :param k:
    :return:
    """
    if l[-1] <= k:
        return -1

    i = len(l) // 2
    start, end = 0, len(l) - 1

    while start < end:
        if l[i] > k:
            end = i
        else:
            start = i + 1
    
        i = start + (end - start) // 2

    return i
