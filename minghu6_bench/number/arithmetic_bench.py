
from minghu6.test.bench import bench


INTS: list[int] = list(
    range(1_000_000_000, 2_000_000_000, 1_000))


@bench
def div_2():
    for i in INTS:
        i // 2


@bench
def div_shift():
    for i in INTS:
        i >> 1


@bench
def mul_2():
    for i in INTS:
        i * 2


@bench
def mul_shift():
    for i in INTS:
        i << 1

