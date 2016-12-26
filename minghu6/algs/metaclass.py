# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
# Some of Useful MetaClass
################################################################################
"""

class singleton_basic(type):
    """
    Select enable Singleton Pattern MetaClass,
    You can customize your select func by define a _getkey in your sub MetaClass.
    _getkey(cls, *args, **kwargs): gather params from args and kwargs,
     return a key(same key means same instance,
                  different key means different instance, of course)
     singleton_basic._getkey return same key always
    """
    def _get_singleton_key(cls, *args, **kwargs):
        """
        you can override this method to customize your Slelect-Singleton Class
        return: key
        """

        return 'Singleton'

    def __init__(cls, name, bases, nmspc):
        super(singleton_basic, cls).__init__(name, bases, nmspc)
        cls.instances= {}

    def __call__(cls, *args, **kwargs):
        instances = cls.instances
        key = cls._get_singleton_key(*args, **kwargs)
        if key not in instances:
            new_instance = super(singleton_basic, cls).__call__(*args, **kwargs)
            instances[key] = new_instance

        return instances[key]


if __name__ == '__main__':
    #ref minghu6_test.algs.metaclass
    pass

