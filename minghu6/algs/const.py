#! /usr/bin/env python3
# -*- coding:utf-8 -*-

class const:

    class ConstError(TypeError):pass
    class ConstCaseError(ConstError):pass

    def __setattr__(self, name, value):
        '''
        const var :only once assignment and consist of UPPERCASE 
        '''
        if name in self.__dict__:
            raise (self.ConstError,
                   "Can't change const.{0:s}".format(name))

        if not name.isupper():
            raise (self.ConstCaseError('const name {0} is not all uppercase'.format(name)))

        self.__dict__[name]=value


import sys
sys.modules[__name__]=const()

