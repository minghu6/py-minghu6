# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

import random

def fast_exp_mod(b, e, m):
    """
    e = e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n)

    b^e = b^(e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n))
        = b^(e0*(2^0)) * b^(e1*(2^1)) * b^(e2*(2^2)) * ... * b^(en*(2^n))

    b^e mod m = ((b^(e0*(2^0)) mod m) * (b^(e1*(2^1)) mod m) * (b^(e2*(2^2)) mod m) * ... * (b^(en*(2^n)) mod m) mod m

    return b^e mod m
    """
    result = 1
    while e != 0:
        if (int(e) & 1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e = int(e) >>1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b*b) % m
    return result


def isprime(n):

    def prime_test(n):

        if n < 2:
            raise Exception('Argument Error')
        elif n == 3:
            return 'prime'


        q = n - 1
        k = 0
        #Find k, q, satisfied 2^k * q = n - 1
        while q % 2 == 0:
            k += 1
            q /= 2
        a = random.randint(2, n-2)
        #If a^q mod n= 1, n maybe is a prime number
        if fast_exp_mod(a, q, n) == 1:
            return "inconclusive"
        #If there exists j satisfy a ^ ((2 ^ j) * q) mod n == n-1, n maybe is a prime number
        for j in range(0, k):
            if fast_exp_mod(a, (2**j)*q, n) == n - 1:
                return "inconclusive"
        #a is not a prime number
        return "composite"

    if n % 2 == 0:
        return False

    #If n satisfy primeTest 10 times, then n should be a prime number
    for i in range(10):
        if prime_test(n) == "composite":
            return False

    return True

def find_prime(end, start=0):

    while True:
        #Select a random number n
        n = random.randint(start, end)
        #print(n)
        if isprime(n): return n


if __name__ == '__main__':

    n = find_prime(1024)
    print(n)