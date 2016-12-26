# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
About decorator
################################################################################
"""
from functools import partial




def require_vars(property_args=list(),method_args=list()):
    """Class decorator to require methods on a subclass.
    pyversion>=2.6
    Example usage
    ------------
    @require_methods(prperty_args=['m1'], method_args=['m2'])
    class C(object):
        'This class cannot be instantiated'
        'unless the subclass defines m1 and m2().'
        def __init__(self):
            pass
    """
    import sys
    if sys.version_info.major==2 and sys.version_info.minor<6:
        raise Exception('python version do not support this decorator')
    def fn(cls):
        orig_init = cls.__init__
        def init_wrapper(self, *args, **kwargs):
            for method in method_args:
                if (not (method in dir(self))) or \
                   (not callable(getattr(self, method))):
                    raise Exception(("Required method %s "
                                     "not implemented") % method)

            for property in property_args:
                if (not (property in dir(self))) or \
                   (callable(getattr(self, property))):
                    raise Exception(("Required property %s "
                                     "not implemented") % property)


            orig_init(self, *args, **kwargs)
        cls.__init__ = init_wrapper
        return cls
    return fn




def exception_handler(*pargs):
    """
    An exception handling idiom using decorators
    Specify exceptions in order, first one is handled first
    last one last.
    """

    def wrapper(f):
        if pargs:
            (handler,li) = pargs
            t = [(ex, handler)
                 for ex in li ]
            t.reverse()
        else:
            t = [(Exception,None)]

        def newfunc(t,*args, **kwargs):#recursion
            ex, handler = t[0]

            try:
                if len(t) == 1:
                    f(*args, **kwargs)
                else:
                    newfunc(t[1:],*args,**kwargs)
            except ex as e:
                if handler:
                    handler(e)
                else:
                    print (e.__class__.__name__, ':', e)

        return partial(newfunc,t)
    return wrapper

def ignore(func):
    """
    ignore all exception,
     Usage: @ignore
            def func():
               #...
               pass

    :param func:
    :return:
    """
    def func_pass(e):
        pass

    return partial(exception_handler, func_pass, Exception)



def singleton(cls):
    """
    More Advanced Select Enable Version can ref metaclass.singleton_basic
    :param cls:
    :return:
    """
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


import time
def timer(label='', unit = 'ms', trace=True): # On decorator args: retain args
    def onDecorator(func):       # On @: retain decorated func
        def onCall(*args, **kargs): # On calls: call original
            start = time.clock() # State is scopes + func attr
            result = func(*args, **kargs)
            elapsed = time.clock() - start
            onCall.alltime += elapsed
            if trace:
                unit_conversion = {'ms' : 1e3,
                                  's' : 1,
                                  'min':1/60,
                                   'h' : 1/(60 * 60)
                                  }

                format = '%s%s: %.5f, %.5f %s'
                values = (label, func.__name__,
                          elapsed*unit_conversion[unit],
                          onCall.alltime*unit_conversion[unit],
                          unit)

                print(format % values)

            return result

        onCall.alltime = 0
        return onCall

    return onDecorator







if __name__ == '__main__':

    @require_vars(property_args=['a'],method_args=['a'])
    class T:
        @property
        def a(self):
            print('haha')

    try:
        T()
    except Exception as e:
        print(e)

    @singleton
    class T2:
        def __init__(self, t=2):
            self.t = t
        pass

    t1=T2()
    #print(t1.t)
    t2=T2()
    assert t1==t2

    def myhandler(e):
        print ('Caught exception!', e)

    # Examples
    # Specify exceptions in order, first one is handled first
    # last one last.

    @exception_handler(myhandler,(ZeroDivisionError,))
    @exception_handler(None,(AttributeError, ValueError))
    def f1():
        1/0

    @exception_handler()
    def f3(*pargs):
        l = pargs
        return l.index(10)

    f1()
    f3()

