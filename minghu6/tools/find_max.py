#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#python 3

"""
search recursion dir and file
"""
import os

import pprint

from sys import argv,exc_info

import re

from argparse import ArgumentParser 

def shell_interactive():
    parser=ArgumentParser()

    
    parser.add_argument('--trace',type=int,choices=[0,1,2],
                       help=('about print 0->close;1->only dir;2-> add file'
                             'default close-0'))
    
    parser.add_argument('--topnum',type=int,
                        help='the number of file which will be echoed ')

    parser.add_argument('-.','--extname',
                        help='default search any form of file such as .py')

    parser.add_argument('-p','--path',dest='dirname',
                        help='searched dir')

    parser.add_argument('--quick',action='store_true',
                        help=('if open the quick search mod (ignore the line search)'
                              'default true'))
    
    parser.add_argument('-pat','--pattern',
                        help='regular matching file name')

    
    args=parser.parse_args()

    from minghu6.algs.dict import remove_value
    return remove_value(args.__dict__,None)
    

def file_search(trace=0,
                topnum=3,
                dirname=os.curdir,
                extname='',
                quick=True,
                pattern='.*',
                inner=False):
    '''
    
    '''  

    def tryprint(arg):
        try:
            print(arg) #the sign can'nt be printed
        except UnicodeEncodeError:
            print(arg.encode()) #try origin str

    visited=set()
    allsizes=[]
    pattern_c=re.compile(pattern)#speed up
    
    for (thisDir,subHere,fileHere) in os.walk(dirname):
        if trace:tryprint(thisDir)
        thisDir=os.path.normpath(thisDir)
        fixname=os.path.normcase(thisDir)
        if fixname in visited: #has visited                                                
            tryprint('skipping  => '+thisDir)
        else:
            visited.add(fixname)
            for filename in fileHere:
                fullname=os.path.join(thisDir,filename)
                if filename.endswith(extname) and pattern_c.findall(filename) != list():
                    ## filename matching
                        
                    if trace>1:tryprint('+++'+filename)
                    
                    
                    try:
                        bytesize=os.path.getsize(fullname) #return file's size
                        bytesize//=1024 #as a KB form              
                        
                        if quick==False:
                            linesize=sum(+1 for line in open(fullname,'rb'))#return line's number
                        else:
                            linesize=0
                        
                    except Exception:
                        print('error',exc_info()[0])
                    else:
                        allsizes.append((bytesize,linesize,fullname))

    """
    print the maxsize of file and maxlinesize of file
    """
    if not inner:
        print('(kb\n',
          'line\n',
          'file)\n')

    max_size=[]
    max_line=[]
    for (title,key) in [('kbytes',0),('lines',1)]:
        if not inner:
            print('\nBy {0:s}...'.format(title))
            
        if title=='lines' and quick:continue
        else:allsizes.sort(key=lambda x:-x[key])

        if title=='kbytes':
            max_size=[s[2] for s in allsizes[:topnum]]
        elif title=='lines':
            max_line=[s[2] for s in allsizes[:topnum]]
            
        if not inner:
            pprint.pprint(allsizes[:topnum])

    
    
    return (max_size,max_line)
    
if __name__=='__main__':

    from minghu6.algs.timeme import timeme
    with timeme() as t:
        args_dict=shell_interactive()
        file_search(**args_dict)

    print('total',t.total,'s')

                    
