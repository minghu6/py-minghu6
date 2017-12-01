# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from minghu6.algs.decorator import ignore


@ignore
def test_singleton_basic():
    from minghu6.algs.metaclass import SingletonBasic

    class Singleton2(SingletonBasic):
        """
        dbname is key for example
        """
        @classmethod
        def _get_singleton_key(cls, *args, **kwargs):
            dbname = args[0] if len(args) > 0 else kwargs['dbname']
            return dbname

    class T(Singleton2):
        def __init__(self, *args, **kw):
            self.a = 1

    # same key same instance
    #assert T('a') is T(dbname='a')

    # different key different instance
    assert T('a') is not T('b')
    assert T('a') is T('a')

    # avoid re __init__
    t1 = T('a')
    t1.a = 3

    t2 = T('a')
    assert t1.a == 3


if __name__ == '__main__':
    test_singleton_basic()
