#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from minghu6.algs.var import isiterable

class dict(dict):

    
    def _remove_value(self, value):
        return remove_value(self, value)
        
    def _remove_key(self, key):
        self=remove_key(self, key)
    pass

def remove_value(dic, values):

    if isiterable(values):

        return {_key:dic[_key] for _key in dic if dic[_key] not in values}
    else:

        return {_key:dic[_key] for _key in dic if dic[_key] != values}


def remove_key(dic, keys):

    if isiterable(keys):

        return {_key:dic[_key] for _key in dic if _key not in keys }

    else:

        return {_key:dic[_key] for _key in dic if _key != keys}

if __name__=='__main__':
    d=dict({0:'a', 1:None, 2:None, 3:'d', None:'a', None:None})

    #d=remove_value(d,None)
    print(d)
    print(d._remove_value(None).values())

    print(remove_value(d,None))

    print(remove_key(d, None))
    print(remove_key(d, {1, 2, 3, None, 0}))