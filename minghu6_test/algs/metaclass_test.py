# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
from minghu6.algs.decorator import ignore


def test_singleton_basic():
    from minghu6.algs.decorator import singleton

    @singleton
    class T:
        """
        dbname is key for example
        """
        @classmethod
        def _get_instance_key(cls, *args, **kwargs):
            dbname = args[0] if len(args) > 0 else kwargs['dbname']
            return dbname

        def __init__(self, *args, **kw):
            self.a = 1

    # same key same instance
    assert T('a') is T(dbname='a')

    # different key different instance
    assert T('a') is not T('b')
    assert T('a') is T('a')

    # avoid re __init__
    t1 = T('a')
    t1.a = 3

    t2 = T('a')
    assert t1.a == 3


def test_generate_custom_meta():
    from minghu6.algs.metaclass import generate_custom_meta
    import sys

    if sys.version_info.major == 3:
        class ExtraAttrStr(str, metaclass=generate_custom_meta(extra_attr={})):
            pass
        pass
    else:
        class ExtraAttrStr(str):
            __meta_class__ = generate_custom_meta(extra_attr={})

    es = ExtraAttrStr('aaa ')
    assert es.strip() == 'aaa'
    assert es.extra_attr == {}


if __name__ == '__main__':
    test_singleton_basic()
    test_generate_custom_meta()
