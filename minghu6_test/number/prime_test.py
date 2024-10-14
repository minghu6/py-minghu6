# -*- coding:utf-8 -*-

from itertools import chain, islice
from random import randrange

from minghu6.itertools import flatten
from minghu6.number.prime import *


def test_prime_sieves():

    def partial_mairson_dual_sieve_factorization(n):
        return iter(mairson_dual_sieve_factorization(n)[0])

    sieves = [
        e_seg_sieve,
        mairson_sieve,
        mairson_sieve_improved,
        mairson_dual_sieve,
        partial_mairson_dual_sieve_factorization,
        wheel_sieve,
        fixed_wheel_seg_sieve,
        fixed_wheel_seg_sieve_mul2add,
        sundram_sieve,
        sundram_sieve_improved,
        atkin_sieve_simple,
        gpf_sieve
    ]

    # special case

    # random number pair test

    rand_list_meta = [
        (1, 10, 3),
        (100, 300, 5),
        (1000, 3000, 3),
        (10_000, 30_000, 3),
    ]

    fixed_list = [169, 1690, 16900]

    rand_list = flatten(
        map(lambda x: [randrange(x[0], x[1]) for _ in range(x[2])], rand_list_meta)
    )

    for n in chain(rand_list, fixed_list):
        std = set(e_sieve(n))

        for f in sieves:
            fname = f.__name__

            fset = set(f(n))

            for i in range(0, n + 1):
                flag = i in std

                assert (
                    i in fset
                ) == flag, f"{fname}: ({i}/{n}) should be {'prime' if flag else 'nonprime'}"

            assert (
                len(std)
            ) == len(fset), \
            f"{fname}: -/{n} should has {len(std)} prime instead {len(fset)}"


def test_bengelloun_sieve_inf():
    n = 169_000

    pris = list(filter(isprime, range(n + 1)))

    for p, res in zip(pris, (islice(bengelloun_sieve_inf(), len(pris)))):
        # print(res)
        assert p == res


def test_prime_inf_sieves():
    n = 169_000

    inf_sieves = [
        e_sieve_inf,
        gpf_sieve_inf
    ]

    inf_sieve_iters = list(map(lambda f: (f.__name__, f()), inf_sieves))
    g = bengelloun_sieve_inf()

    for _ in range(n + 1):
        p = next(g)

        for name, iter in inf_sieve_iters:
            p0 = next(iter)

            assert p0 == p, f"{name}: expect {p} found {p0}"


if __name__ == "__main__":
    test_bengelloun_sieve_inf()
    test_prime_sieves()
