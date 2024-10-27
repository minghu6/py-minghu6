
from functools import partial, wraps
import inspect


def handle_exception(exception_handler, exception_classes):
    """
    An exception handling idiom using decorators
    Specify exceptions in order, first one is handled first
    last one last.
    >>> def handler(ex):
    ...     print(ex, type(ex))
    ...     return ex.args
    >>> from collections import OrderedDict
    >>> @handle_exception(handler, Exception)
    ... def f():
    ...     d=OrderedDict()
    ...     d['a']=1
    ...     d['b']=2
    ...     raise Exception([1, 2, '3'], d)
    >>> f()
    Traceback (most recent call last):
        ...
    Exception: ([1, 2, '3'], OrderedDict({'a': 1, 'b': 2}))
    >>> @handle_exception(handler, (FileExistsError, FileNotFoundError))
    ... def f2():
    ...     raise FileNotFoundError('abc.txt')
    >>> f2()
    Traceback (most recent call last):
        ...
    FileNotFoundError: abc.txt
    """

    # update meta info to f
    @wraps
    def wrapper(f):
        nonlocal exception_classes

        if inspect.isclass(exception_classes):
            exception_classes = [exception_classes]

        exception_chain = list(exception_classes)
        exception_chain.reverse()  # for recursive invokation

        def newfunc(exception_chain, *args, **kwargs):  # recursion
            exception_class = exception_chain[0]

            try:
                if len(exception_chain) == 1:
                    result = f(*args, **kwargs)
                else:
                    result = newfunc(
                        exception_chain[1:], *args, **kwargs
                    )  # spread exception
            except exception_class as ex:
                return exception_handler(ex)
            else:
                return result

        return partial(newfunc, exception_chain)

    return wrapper


def cli_handle_exception(exception_handler, exception_classes):
    """
    deal with exception stack info, and then just throw the wrapper exception by cli
    >>> def cli_handler1(ex):
    ...     assert False, "Need root permission"
    ...
    >>> @cli_handle_exception(cli_handler1, ZeroDivisionError)
    ... def f():
    ...     1 / 0
    >>> f()
    Traceback (most recent call last):
        ...
    AssertionError: Need root permission
    """
    import inspect
    from functools import partial

    def wrapper(f):
        nonlocal exception_classes

        if inspect.isclass(exception_classes):
            exception_classes = [exception_classes]

        exception_chain = list(exception_classes)
        exception_chain.reverse()  # for recursive invokation

        def newfunc(exception_chain, *args, **kwargs):  # recursion
            exception_class = exception_chain[0]
            raised_exception = None
            try:
                if len(exception_chain) == 1:
                    result = f(*args, **kwargs)
                else:
                    result = newfunc(
                        exception_chain[1:], *args, **kwargs
                    )  # spread exception
            except exception_class as ex:
                raised_exception = (
                    ex  # goto next exception_handler to clean old exception stack.
                )
            else:
                return result

            exception_handler(raised_exception)

        return partial(newfunc, exception_chain)

    return wrapper
