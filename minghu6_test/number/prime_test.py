# -*- coding:utf-8 -*-

from itertools import islice

def test_bengelloun_sieve_inf():
    from minghu6.number.prime import isprime, bengelloun_sieve_inf

    n = 1690

    pris = list(filter(isprime, range(n+1)))

    for p, res in zip(pris, (islice(bengelloun_sieve_inf(), len(pris)))):
        # print(res)
        assert p == res

if __name__ == '__main__':
    test_bengelloun_sieve_inf()
