# -*- coding:utf-8 -*-
#!/usr/bin/env python3

def is_power_2_natrual(n):
    '''
    only for Natural number 1,+2,+4,,+8,...
    '''
    if not isinstance(n,int) or n<=0:
        raise Exception('Not an Natural Number')    

    return not(n&(n-1))

def is_power(n,m):
    '''
    judge if n is power of m;(n>0,m>1)
    '''
    import math
    result=math.log(m,n)
    
    if m<=1 or n<=0:
        raise Exception('\n\tInvalid parameter ! \n\tBe Sure:p1>0 p2>1')
    return int(result)==result


if __name__=='__main__':
    print(is_power_2_natrual(1024))
    print(is_power(1024,2))
    
