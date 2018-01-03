# -*- coding:utf-8 -*-
# !/usr/bin/env python3
"""
################################################################################
# Some of Useful MetaClass
################################################################################
"""
import sys


__all__ = ['SingletonBasic', 'generate_custom_meta']


def generate_custom_meta(**extra_attr):
    class CustomMeta(type):
        def __new__(cls, name, bases, attrs):
            attrs.update(extra_attr)
            return type.__new__(cls, name, bases, attrs)

    return CustomMeta


if sys.version_info.major == 3 and sys.version_info.minor >= 5:
    class SingletonBasic:
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__()

            cls.instances = {}
            cls.__call__ = cls.__call__
            cls._get_singleton_key = cls._get_singleton_key

        def __call__(cls, *args, **kwargs):
            instances = cls.instances
            key = cls._get_singleton_key(*args, **kwargs)
            if key not in instances:
                new_instance = super.__call__(*args, **kwargs)
                instances[key] = new_instance
    
            return instances[key]
        
        @classmethod
        def _get_singleton_key(cls):
            """you can override this method to customize your Slelect-Singleton Class
            return: key
            """
    
            return 'Singleton'
        
        pass


else:
    class SingletonBasic():
        """
        Select enable Singleton Pattern MetaClass,
        You can customize your select func by define a _getkey in your sub MetaClass.
        _getkey(cls, *args, **kwargs): gather params from args and kwargs,
         return a key(same key means same instance,
                      different key means different instance, of course)
         singleton_basic._getkey return same key always
        """
    
        @classmethod
        def _get_singleton_key(mcs, *args, **kwargs):
            """
            you can override this method to customize your Slelect-Singleton Class
            return: key
            """
    
            return 'Singleton'
    
        def __init__(cls, name, bases, nmspc):
            super().__init__(name, bases, nmspc)
            cls.instances = {}
    
        def __call__(cls, *args, **kwargs):
            instances = cls.instances
            key = cls._get_singleton_key(*args, **kwargs)
            if key not in instances:
                new_instance = super().__call__(*args, **kwargs)
                instances[key] = new_instance
    
            return instances[key]


if __name__ == '__main__':
    # ref minghu6_test.algs.metaclass
    pass
