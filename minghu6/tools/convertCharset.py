#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
v1.0
convert a file from charset1 to charset2 if possible
simplified chinese windows :gbk
linux :utf8
"""

import os
from random import random
from time import time


def shell_interactive():
    from argparse import ArgumentParser
    parser=ArgumentParser()

    parser.add_argument('--from',dest='src',
                        help='sourse file site')

    parser.add_argument('--to',dest='dst',
                        help='destination file site(default = from)')

    parser.add_argument('--src_char',dest='from_charset',
                        help='source file charater set')

    parser.add_argument('--dst_char',dest='to_charset',
                        help='destination file charater set')

    parser.add_argument('--chmod',action='store_true',
                        help='chmod to 777')

    


    args=parser.parse_args()

    from minghu6.algs.dict import remove_value
    return remove_value(args.__dict__,None)
    
    
def convertCharset(src,dst=None,from_charset='utf8',
                   to_charset='gbk',chmod=False):

    if chmod==True:
        os.chmod(src,0o777)
        
    try:
        fsrc=open(src, 'rb')
        allmsg = fsrc.readlines()
        fsrc.close()
    except FileNotFoundError:
        print('%s not found'%(src))
        return

    if dst==None:
        dst = src

    try:
        fdst=open(dst, 'wb')
        for line in allmsg:
            fdst.write(line.decode(from_charset).encode(to_charset))
    except FileExistsError:
        print('%s has existed'%dst)
    except UnicodeDecodeError as ex:
        print(ex)
        fdst.close()
        with open(dst,'wb') as fdst:
            fdst.writelines(allmsg)



if __name__=='__main__':
    
    args_dict=shell_interactive()
    convertCharset(**args_dict)
    
    
                
            
    
