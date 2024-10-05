# -*- coding:utf-8 -*-

from itertools import chain, islice
from random import randrange

from minghu6.itertools import flatten
from minghu6.number.prime import *


def test_prime_sieves():

    norm_functions = [e_seg_sieve]

    inf_functions = [bengelloun_sieve_inf]

    # special case

    # random number pair test

    rand_list = [
        (1, 10, 3),
        (100, 300, 5),
        (1000, 3000, 3),
        (10_000, 30_000, 3),
    ]

    fixed_list = [169, 1690, 1690]

    test_list = flatten(map(
        lambda x: [randrange(x[0], x[1]) for _ in range(x[2])], rand_list
    ))

    for n in chain(fixed_list, test_list):
        std = set(e_sieve(n))

        for f in norm_functions:
            fname = f.__name__

            fset = set(f(n))

            for i in range(0, n + 1):
                flag = i in std

                assert (
                    i in fset
                ) == flag, f"{fname}: ({i}/{n}) should be { 'prime' if flag else 'nonprime' }"


def test_bengelloun_sieve_inf():
    from minghu6.number.prime import isprime, bengelloun_sieve_inf

    n = 1690

    pris = list(filter(isprime, range(n + 1)))

    for p, res in zip(pris, (islice(bengelloun_sieve_inf(), len(pris)))):
        # print(res)
        assert p == res


if __name__ == "__main__":
    test_bengelloun_sieve_inf()
    test_prime_sieves()
