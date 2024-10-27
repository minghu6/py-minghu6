
from contextlib import redirect_stdout
from io import StringIO

from minghu6.test.profile import *
from minghu6.datetime import TimeUnit


def test_timer():
    # Test on functions
    @timer(trace=True, label="[CCC]==>")
    def listcomp(N):  # Like listcomp = timer(...)(listcomp)
        return [x * 2 for x in range(N)]  # listcomp(...) triggers onCall

    @timer(trace=True, label="[MMM]==>", unit=TimeUnit.SEC)
    def mapcall(N):
        return list(map((lambda x: x * 2), range(N)))  # list() for 3.0 views

    for func in (listcomp, mapcall):
        buff = StringIO()
        with redirect_stdout(buff):
            result = func(5)  # Time for this call, all calls, return value

        if func is listcomp:
            assert buff.getvalue().startswith("[CCC]==>listcomp")
        elif func is mapcall:
            assert buff.getvalue().startswith("[MMM]==>mapcall")

        assert result == [0, 2, 4, 6, 8]
        assert isinstance(func.alltime, (float, int))  # Total time for all calls

        # Test on methods

    class Person:
        def __init__(self, name, pay):
            self.name = name
            self.pay = pay

        @timer()
        def give_raise(self, percent):  # giveRaise = timer()(giveRaise)
            self.pay *= 1.0 + percent  # tracer remembers giveRaise

        @timer(label="**")
        def last_name(self):  # lastName = timer(...)(lastName)
            return self.name.split()[-1]

    bob = Person("Bob Smith", 50000)
    sue = Person("Sue Jones", 100000)

    buff = StringIO()
    with redirect_stdout(buff):
        bob.give_raise(0.10)

    assert buff.getvalue().startswith("give_raise")
    print(buff.getvalue())

    with redirect_stdout(buff):
        sue.give_raise(0.20)  # runs onCall(sue, .10)

    assert (int(bob.pay), int(sue.pay)) == (55000, 120000)
    buff = StringIO()
    with redirect_stdout(buff):
        assert (bob.last_name(), sue.last_name()) == ("Smith", "Jones")

    assert buff.getvalue().startswith("**last_name")
