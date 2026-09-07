# -*- coding:utf-8 -*-

import atexit
from collections.abc import Callable
from functools import partial, wraps
from typing import Any
from exports import export

from minghu6.string import camelize


################################################################################
#### Decorators

_SINGLETON_EXIT = '__singleton_exit__'
_SINGLETON_KEY = '__singleton_key__'


def _getattrs(obj) -> dict[str, Any]:
    return dict(map(lambda name: (name, getattr(obj, name)), dir(obj)))


def _annotate_tag[T](obj: T, key: str) -> T:
    if hasattr(obj, key):
        raise ValueError(f'override existed attribute {key}')

    setattr(obj, key, True)

    return obj


def _find_tagged(obj, key: str) -> list[tuple[str, object]]:
    res = []

    for name, attr in _getattrs(obj).items():
        if getattr(attr, key, False):
            res.append((name, attr))

    return res


@export
def singleton_key(f: Callable):
    """ Annotate get_instance_key """

    return _annotate_tag(f, _SINGLETON_KEY)


@export
def singleton_exit(f: Callable):
    """ Annotate exit method for `atexit` """

    return _annotate_tag(f, _SINGLETON_EXIT)


@export
def singleton(cls):
    """
    Supply more flexiable control than using a MetaClass.

    :param cls:
    :return:

    >>> @singleton
    ... class T1:
    ...     pass

    >>> assert T1() is T1()

    >>> @singleton
    ... class T2:
    ...    @singleton_key
    ...    def _get_instance_key(a, b):
    ...         return b
    ...    def __init__(self, a, b):
    ...        pass

    >>> assert T2(1, 1) is T2(2, 1)
    >>> assert T2(1, 1) is not T2(1, 2)
    """

    instances = {}

    def _default_get_instance_key(*args, **kwargs):
        return

    # refer https://docs.python.org/3/library/functools.html#functools.update_wrapper
    @wraps(cls)
    def _singleton(*args, **kw):
        """ Class like object """

        # search instancekey tag

        keys = _find_tagged(cls, _SINGLETON_KEY)

        if len(keys) > 1:
            raise ValueError(f'duplicated instancekey annotations {keys}')

        if keys:
            get_instance_key = keys[0][1]
        else:
            get_instance_key = _default_get_instance_key

        instance_key = get_instance_key(*args, **kw)

        if instance_key not in instances:
            instance = cls(*args, **kw)

            # search exit tag

            exit_list = _find_tagged(cls, _SINGLETON_EXIT)

            if len(exit_list) > 1:
                raise ValueError(f'duplicated exit annotations {exit_list}')

            if exit_list:
                exit_func = exit_list[0][1]
                atexit.register(partial(exit_func, instance))

            instances[instance_key] = instance

        return instances[instance_key]

    # apply cls method to `pseudo class` function
    for name, attr in _getattrs(cls).items():
        if not (name.startswith("__") and name.endswith("__")):
            setattr(_singleton, name, attr)

    return _singleton


@export
def metaclass_append_attributes(**extra_attrs):
    """ Refer [PEP-3115](https://peps.python.org/pep-3115/) """
    class CustomMeta(type):
        def __new__(cls, name, bases, attrs):
            attrs.update(extra_attrs)
            return type.__new__(cls, name, bases, attrs)

    return CustomMeta
