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

def timer_test():
    from minghu6.algs.decorator import timer


    # Test on functions
    @timer(trace=True, label='[CCC]==>')
    def listcomp(N): # Like listcomp = timer(...)(listcomp)
        return [x * 2 for x in range(N)] # listcomp(...) triggers onCall
    @timer(trace=True, label='[MMM]==>', unit='s')
    def mapcall(N):
        return list(map((lambda x: x * 2), range(N))) # list() for 3.0 views

    for func in (listcomp, mapcall):
        result = func(5) # Time for this call, all calls, return value
        func(5000000)
        print(result)
        print('allTime = %s\n' % func.alltime) # Total time for all calls

        # Test on methods
    class Person:
        def __init__(self, name, pay):
            self.name = name
            self.pay = pay
        @timer()
        def giveRaise(self, percent): # giveRaise = timer()(giveRaise)
            self.pay *= (1.0 + percent) # tracer remembers giveRaise
        @timer(label='**')
        def lastName(self): # lastName = timer(...)(lastName)
            return self.name.split()[-1]

    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)
    bob.giveRaise(.10)
    sue.giveRaise(.20) # runs onCall(sue, .10)
    print(bob.pay, sue.pay)
    print(bob.lastName(), sue.lastName()) # runs onCall(bob), remembers lastName
    print('%.5f %.5f' % (Person.giveRaise.alltime, Person.lastName.alltime))




if __name__ == '__main__':

    require_vars_test()
    exception_handler_test()
    singleton_test()
    ignore_test()
    timer_test()
    pass