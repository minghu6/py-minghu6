# -*- coding:utf-8 -*-

from minghu6.metaclass import *


def test_singleton_basic():
    @singleton
    class T:
        """
        dbname is key for example
        """

        @singleton_key
        def _get_instance_key(*args, **kwargs):
            dbname = args[0] if len(args) > 0 else kwargs["dbname"]
            return dbname

        def __init__(self, *args, **kw):
            self.a = 1

    # same key same instance
    assert T("a") is T(dbname="a")

    # different key different instance
    assert T("a") is not T("b")
    assert T("a") is T("a")

    # avoid re __init__
    t1 = T("a")
    t1.a = 3

    t2 = T("a")

    assert t1.a == 3


def test_generate_custom_meta():
    import sys

    if sys.version_info.major == 3:

        class ExtraAttrStr(str, metaclass=metaclass_append_attributes(extra_attr={})):
            pass

        pass
    else:

        class ExtraAttrStr(str):
            __meta_class__ = metaclass_append_attributes(extra_attr={})

    es = ExtraAttrStr("aaa ")
    assert es.strip() == "aaa"
    assert es.extra_attr == {}


if __name__ == "__main__":
    test_singleton_basic()
    test_generate_custom_meta()
