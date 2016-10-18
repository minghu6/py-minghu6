# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""



def require_vars_test():
    from minghu6.algs.decorator import require_vars

    @require_vars(property_args=['a'],method_args=['a'])
    class T:
        @property
        def a(self):
            print('haha')

    try:
        T()
    except Exception as e:
        assert e.__str__() == ('Required method a not implemented')
    else:
        assert False, 'There should be an Exception'


def exception_handler_test():
    from minghu6.algs.decorator import exception_handler

    def myhandler(e):
        print ('Caught exception!', e)

    # Examples
    # Specify exceptions in order, first one is handled first
    # last one last.

    @exception_handler(myhandler,(ZeroDivisionError,))
    def f1():
        1/0

    @exception_handler()
    def f3(*pargs):
        l = pargs
        return l.index(10)

    f1()
    f3()

def ignore_test():
    from minghu6.algs.decorator import ignore
    @ignore
    def f1():
        1/0

    f1()

def singleton_test():
    from minghu6.algs.decorator import singleton

    @singleton
    class T2():
        pass

    t1=T2()
    t2=T2()
    assert t1==t2


if __name__ == '__main__':

    require_vars_test()
    exception_handler_test()
    singleton_test()
    ignore_test()
    pass