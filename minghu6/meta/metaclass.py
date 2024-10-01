# -*- coding:utf-8 -*-

__all__ = ['generate_custom_meta']


def generate_custom_meta(**extra_attr):
    class CustomMeta(type):
        def __new__(cls, name, bases, attrs):
            attrs.update(extra_attr)
            return type.__new__(cls, name, bases, attrs)

    return CustomMeta


if __name__ == '__main__':
    # ref minghu6_test.algs.metaclass
    pass
