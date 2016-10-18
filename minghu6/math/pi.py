# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
some method to calculate π
################################################################################
"""
import random
import math

def using_rectangles(N=int(10e4)):
    n=0
    for i in range(N):
        x=random.random()
        y=random.random()
        if x*x+y*y<1:
            n+=1

    return 4*n/N


def using_Monte_Carlo_method(N=int(10e4)):
    return using_rectangles(N)

def random_sampling(N=int(10e4)):
    return using_rectangles(N)



def using_trapezoidal(N=int(10e4)):
    """

    :return:
    """

    def sub_sum():
        for j in range(1,N):
            x=-1+j*2/N
            yield (1-x**2)**0.5

    return 4*sum(sub_sum())/N



if __name__=='__main__':
    from minghu6.algs import timeme

    with timeme.timeme() as tm1:
        pi1=using_rectangles(int(10e5))
        print('using_rectangles', pi1)

    with timeme.timeme() as tm2:
        pi2=using_trapezoidal(int(10e5))
        print('using_trapezoidal', pi2)

    print('tm1: ',tm1)
    print('tm2: ',tm2)
