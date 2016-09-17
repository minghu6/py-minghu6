#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
chop a big size of file
"""
import sys,os
from pprint import pprint
todir=os.path.join(os.getcwd(),'temp')
kilobytes=1024
megabytes=kilobytes*1000
chunksize=int(1.4*megabytes) #size of softdisk

def split(fromfile,todir=todir,chunksize=chunksize):
    if not os.path.exists(todir):
        os.mkdir(todir) # create a new dir if the target dir doesn't exist
    else:
        for fname in os.listdir(todir):#delete all files which has existed before
            os.remove(os.path.join(todir,fname))

    partnum=0
    __input=open(fromfile,'rb')#read as a binary form
    while True:
        chunk=__input.read(chunksize)#get next part
        if not chunk:break #over
        partnum+=1
        filename=os.path.join(todir,'part{0:05d}'.format(partnum)) ##join after base on filename
        fileobj=open(filename,'wb')
        fileobj.write(chunk)
        fileobj.close()

    __input.close()
    assert partnum<=99999 #raise asserterror if the partnum>=1,000,000(about 100GB)
    return partnum

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='-help':
        pprint('Use: chopfile [split the file to target-dir [chunksize]\nchopfile fromfile todir chunksize(-option)')

    else:
        if len(sys.argv)<3:
            interactive=True##
            fromfile=input('File to split?') ### equal to raw_input() in 2.x
            todir_tmp=input('Directory to store part file?')
            chunksize_tmp=input('Chunksize(kbyte)?')
            if todir_tmp !='':todir=todir_tmp
            if chunksize_tmp!='':chunksize=1024*eval(chunksize_tmp)
        else:
            interactive=False##
            fromfile,todir=sys.argv[1:3] #equal to argv[1] argv[2]
            if len(sys.argv)==4:chunksize=1024*eval(sys.argv[3])
            
        absfrom,absto=map(os.path.abspath,[fromfile,todir])
        pprint('Splitting {0:s} to {1:s} by {2:d}'.format(absfrom,absto,chunksize))

        try:
            parts=split(fromfile,todir,chunksize)
        except:
            print('Error during split:')
            print(sys.exc_info()[0],sys.exc_info()[1])
        else:
            print('Split finished:',parts,'parts are in ',absto)

        if interactive:input('Press Enter key') #kit the script,stop here
            
        

  







