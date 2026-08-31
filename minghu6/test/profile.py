
import time

from exports import export

from minghu6.datetime import TimeUnit


################################################################################
#### Decorators

@export
def timer(label: str ="", unit: TimeUnit = TimeUnit.MILLI, trace=True):  # On decorator args: retain args
    import time

    def on_decorator(func):  # On @: retain decorated func
        def on_call(*args, **kargs):  # On calls: call original
            start = time.perf_counter()  # State is scopes + func attr
            result = func(*args, **kargs)
            elapsed = time.perf_counter() - start
            on_call.alltime += elapsed
            if trace:
                format = "%s%s: %.5f, %.5f %2s"
                values = (
                    label,
                    func.__name__,
                    elapsed * unit.value,
                    on_call.alltime * unit.value,
                    unit.format_short(),
                )

                print(format % values)

            return result

        on_call.alltime = 0
        return on_call

    return on_decorator


################################################################################
#### Context Managers

@export
class Watch:
    def __init__(self, fmt=".2f") -> None:
        """
        :fmt: format float number of (s/ms/us)
        """
        self.fmt = fmt

    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter_ns()
        self._nanos = self.end - self.start

    @property
    def nanos(self) -> int:
        return self._nanos

    @property
    def micros(self) -> float:
        return self._nanos / TimeUnit.MICRO.value

    @property
    def millis(self) -> float:
        return self._nanos / TimeUnit.MILLI.value

    @property
    def secs(self) -> float:
        return self._nanos / TimeUnit.SEC.value
