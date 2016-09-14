# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""


def singleton_basic_test():
    from minghu6.algs.metaclass import singleton_basic

    class singleton_2(singleton_basic):
        """
        dbname is key for example
        """
        def _getkey(cls, *args, **kwargs):

            dbname = args[0] if len(args)>0 else kwargs['dbname']
            return dbname

    class T(metaclass=singleton_2):
        def __init__(self, *args, **kw):
            print(args, kw)

    assert T('a') is T(dbname='a')

    assert T('a') is not T('b')


if __name__ == '__main__':

    singleton_basic_test()