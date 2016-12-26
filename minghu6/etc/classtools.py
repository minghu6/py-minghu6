#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Assorted class tools
'''
class AttrDisplay:
    '''
    Provides an inheritable print overload method that displays 
    instances with their class names ATTand a name=value pair for
    each attribute stored on the instance itself
    '''
    def gatherAttrs(self):
        attrs=[]
        for key in sorted(self.__dict__):
            attrs.append('{0:s}={1:d}'.format(key, getattr(self, key)))

        return ', '.join(attrs)

    def __str__(self):
        return '[{0:s},{1:s}]'.format(self.__class__.__name__,self.gatherAttrs())

if __name__=='__main__':
    class TopTest(AttrDisplay):
        count=0
        def __init__(self):
            self.attr1=TopTest.count
            self.attr2=TopTest.count+1
            TopTest.count+=2
    class SubTest(TopTest):
        pass

    X,Y =TopTest(), SubTest()
    print(X)
    print(Y)

        
