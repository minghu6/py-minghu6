
from functools import partial, wraps

from exports import export

from minghu6.etc.error import handle_exception


#################################################################################
#### Decorators

@export
def assert_exception(exception):
    @wraps
    def wrapper(func):
        def new_func():
            assert_true = False
            exception_received = None

            try:
                func()
            except exception:
                pass
            except Exception as ex:
                assert_true = True
                exception_received = ex

            if assert_true:
                raise AssertionError(exception_received)

        return new_func

    return wrapper


@export
def suppress(f):
    """
    suppress all exceptions,

    :param f:
    :return:
    >>> @suppress
    ... def f1():
    ...    1 / 0
    >>> _ = f1()
    """

    def func_pass(ex):
        pass

    return partial(handle_exception, func_pass, Exception)


@export
def mock_func(*return_args, **return_kwargs):
    """
    >>> @mock_func(1, 2, c=3)
    ... def f():
    ...     print("hi?")
    ...     return "abc"
    >>> assert f() == (1, 2, 3)
    """
    def wrapper(f):
        def inner(*inner_args, **inner_kwargs):
            if not return_args and not return_kwargs:
                return None
            else:
                return return_args + tuple(return_kwargs.values())

        return inner

    return wrapper


@export
def passit(f):
    """
    >>> @passit
    ... def f():
    ...    print("hello, can you listen me?!")
    ...    return "!!"
    >>> assert f() is None
    """
    return mock_func()(f)
