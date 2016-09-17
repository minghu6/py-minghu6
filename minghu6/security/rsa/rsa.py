# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
RSA Implemets
################################################################################
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



def find_prime(key_half_length):

    while True:
        #Select a random number n
        n = random.randint(0, 1<< key_half_length)
        #print(n)
        if isprime(n): return n


def extendedGCD(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x , y , q = extendedGCD( b , a % b )
        x , y = y, ( x - (a // b) * y )
        return x, y, q


def selectE(fn, key_half_length):
    assert isinstance(fn, int) and fn >1
    while True:
        #e and fn are relatively prime
        e = random.randint(0, 1<<key_half_length)
        #e = random.randint(0, fn-1)
        (x, y, r) = extendedGCD(e, fn)
        if r == 1:
            return e

def computeD(fn, e):
    (x, y, r) = extendedGCD(fn, e)
    #y maybe < 0, so convert it
    if y < 0:
        return fn + y
    return y

def key_generation(key_length = 64, pq_pair=None):
    """
    #Encrypt unit length must < (n = p*q)!!
    :param key_length:
    :param pq_pair:
    :return:
    """
    #generate public key and private key
    if pq_pair == None:
        while True:
            p = find_prime(key_length//2)
            q = find_prime(key_length//2)

            if p != q:
                break
    else:
        (p, q) = pq_pair

    #print(p,q)
    n = p * q
    fn = (p-1) * (q-1)
    e = selectE(fn, key_length//2)
    d = computeD(fn, e)

    #print(e, d)
    return (n, e, d)

def output_key(n, e, d):
    pass

def encryption(M, e, n):
    #RSA C = M^e mod n
    return fast_exp_mod(M, e, n)

def decryption(C, d, n):
    #RSA M = C^d mod n
    return fast_exp_mod(C, d, n)


def encryp_str(M, e, n):
    """

    :param M: Plain Text
    :param e: (E, N) Public Key
    :param n: (E, N) Public Key
    :return:  Cryptted Message
    """

    assert isinstance(M, str)

    C = ''.join([hex(encryption(ord(u), e, n)) for u in M])

    return C
    pass

def decryp_str(C, d, n):
    """

    :param C: Crypt Message
    :param d: (D, E) Private Key
    :param n: (D, E) Private Key
    :return:
    """

    assert isinstance(C, str)

    C = C.lower().split('0x')[1:]

    M = ''.join([chr(decryption(int(i, base=16), d, n)) for i in C])

    return M
    pass



def __test_basic():

    """

    :return:
    """

    #X must < n!!
    (n, e, d) = key_generation(64)
    X = random.randint(0, 1<<32)

    print(n,'\n', e,'\n', d)

    C = encryption(X, e, n)
    M = decryption(C, d, n)
    print ("PlainText:", X)
    print ("Encryption of plainText:", C)
    print ("Decryption of cipherText:", M)
    print ("The algorithm is correct:", X == M)

def __lab_test():
    (p ,q) = (47, 59)
    pq_pair=(p ,q)
    (n, e, d) = key_generation(pq_pair=(p ,q))
    m = 465
    print('origin m:',m, 'n:',n)
    C = encryption(m, e, n)
    print('C: ',C)

    m = decryption(C, d, n)
    print('m: ',m)


def __test_str():

    (n, e, d) = key_generation(64)

    X = 'Hello, 明文'
    print ("PlainText:", X)

    C = encryp_str(X, e, n)
    print ("Encryption of plainText:", C)

    M = decryp_str(C, d, n)
    print ("Decryption of cipherText:", M)
    print ("The algorithm is correct:", X == M)




if __name__ == '__main__':

    __test_basic()
    #__test_str()
    #__lab_test()
    pass