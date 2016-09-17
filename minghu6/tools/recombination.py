#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
 next of chopfile
"""

import os,sys
from pprint import pprint
readsize=1024
fromdir=os.path.join(os.getcwd(),'temp')
tofile='out.tmp'

def join(fromdir=fromdir,tofile=tofile):
    output=open(tofile,'wb')
    parts=os.listdir(fromdir)
    parts.sort() ###because of its recombination base on file name...
    for filename in parts:
        filename=os.path.join(fromdir,filename)
        fileobj=open(filename,'rb')
        while True:
            filebytes=fileobj.read(readsize)
            if not filebytes:break
            output.write(filebytes)
        fileobj.close()
    output.close()


if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='-help':
        pprint('Use:recombination [fromdirname todirname]\nrecombination fromdir tofile')

    else:
        if len(sys.argv)!=3:
            interactive=True
            fromdir_tmp=input('Directory containning part files?')
            tofile_tmp=input('Name of file to be recreated?')
            if fromdir_tmp!='':fromdir=fromdir_tmp
            if tofile_tmp!='':tofile=tofile_tmp
        else:
            interactive=False
            fromdir,tofile=sys.argv[1:]
            
        absfrom,absto=map(os.path.abspath,[fromdir,tofile])##print absolute infomation
        pprint('Recombinating {0:s} to make {1:s}'.format(absfrom,absto))

        try:
            join(fromdir,tofile)
        except:
            print('Error joining files:')
            print(sys.exc_info()[:2])
        else:
            pprint('Recombination complete:see {0:s}'.format(absto))

        if interactive:input('Press Enter key') #stop a while
      
    
