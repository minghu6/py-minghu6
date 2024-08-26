# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""


from itertools import islice


def test_gcd():
    from minghu6.math.prime import gcd
    assert gcd(1920, 1080) == 120

def test_bengelloun_sieve_inf():
    from minghu6.math.prime import isprime, bengelloun_sieve_inf

    n = 1690

    pris = list(filter(isprime, range(n+1)))

    for p, res in zip(pris, (islice(bengelloun_sieve_inf(), len(pris)))):
        # print(res)
        assert p == res

if __name__ == '__main__':
    test_gcd()
    test_bengelloun_sieve_inf()
