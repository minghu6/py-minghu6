# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from contextlib import redirect_stdout

from io import StringIO


def test_require_vars():
    from minghu6.algs.decorator import require_vars, LackMethodError

    @require_vars(property_args=['a'], method_args=['a'])
    class T:
        @property
        def a(self):
            tmpvar = 'haha'
            return tmpvar

    try:
        T()
    except LackMethodError as e:
        assert e.__str__() == ('Required method `a` not implemented')
    else:
        assert False, 'There should be an Exception'


def test_exception_handler():
    from minghu6.algs.decorator import exception_handler

    def myhandler(e):
        print('Caught exception!', e)

    # Examples
    # Specify exceptions in order, first one is handled first
    # last one last.

    @exception_handler(myhandler, (ZeroDivisionError,))
    def f1():
        1 / 0

    @exception_handler()
    def f3(*pargs):
        l = pargs
        return l.index(10)

    buff = StringIO()
    with redirect_stdout(buff):
        f1()

    assert buff.getvalue() == 'Caught exception! division by zero\n'

    buff = StringIO()
    with redirect_stdout(buff):
        f3()
    assert buff.getvalue() == 'ValueError : tuple.index(x): x not in tuple\n'


def test_handle_excpetion():
    import doctest
    from minghu6.algs.decorator import handle_exception
    doctest.run_docstring_examples(handle_exception, locals())


def test_ignore():
    from minghu6.algs.decorator import ignore

    @ignore
    def f1():
        1 / 0

    f1()


def test_skip():
    from minghu6.algs.decorator import skip

    @skip
    def f():
        print('hello, can you listen me?!')
        return '!!'

    assert f() is None


def test_mock_func():
    from minghu6.algs.decorator import mock_func

    @mock_func(1, 2, c=3)
    def f():
        print('hi?')
        return 'abc'

    assert f() == (1, 2, 3)


def test_singleton():
    from minghu6.algs.decorator import singleton

    @singleton
    class T2():
        pass

    t1 = T2()
    t2 = T2()
    assert t1 == t2


def test_timer():
    from minghu6.algs.decorator import timer

    # Test on functions
    @timer(trace=True, label='[CCC]==>')
    def listcomp(N):  # Like listcomp = timer(...)(listcomp)
        return [x * 2 for x in range(N)]  # listcomp(...) triggers onCall

    @timer(trace=True, label='[MMM]==>', unit='s')
    def mapcall(N):
        return list(map((lambda x: x * 2), range(N)))  # list() for 3.0 views

    for func in (listcomp, mapcall):
        buff = StringIO()
        with redirect_stdout(buff):
            result = func(5)  # Time for this call, all calls, return value

        if func is listcomp:
            assert buff.getvalue().startswith('[CCC]==>listcomp')
        elif func is mapcall:
            assert buff.getvalue().startswith('[MMM]==>mapcall')

        assert result == [0, 2, 4, 6, 8]
        assert isinstance(func.alltime, (float, int))  # Total time for all calls

        # Test on methods

    class Person:
        def __init__(self, name, pay):
            self.name = name
            self.pay = pay

        @timer()
        def give_raise(self, percent):  # giveRaise = timer()(giveRaise)
            self.pay *= (1.0 + percent)  # tracer remembers giveRaise

        @timer(label='**')
        def last_name(self):  # lastName = timer(...)(lastName)
            return self.name.split()[-1]

    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)

    buff = StringIO()
    with redirect_stdout(buff):
        bob.give_raise(.10)

    assert buff.getvalue().startswith('give_raise')
    print(buff.getvalue())

    with redirect_stdout(buff):
        sue.give_raise(.20)  # runs onCall(sue, .10)

    assert (int(bob.pay), int(sue.pay)) == (55000, 120000)
    buff = StringIO()
    with redirect_stdout(buff):
        assert ((bob.last_name(), sue.last_name()) == ('Smith', 'Jones'))

    assert buff.getvalue().startswith('**last_name')


def test_to_class():
    from minghu6.algs import decorator

    @decorator.to_class('get_result')
    def class_a(pa, pb, pc=3):
        return pa+pb+pc, pa*pb*pc

    ClassA = class_a

    result1 = ClassA(1, 2, 3).get_result()
    assert result1 == (6, 6), result1

if __name__ == '__main__':
    test_require_vars()
    test_exception_handler()
    test_singleton()
    test_ignore()
    test_skip()
    test_mock_func()
    test_timer()
    test_to_class()
    test_handle_excpetion()
