# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
Find
"""

from argparse import ArgumentParser
from pprint import pprint


from minghu6.etc.find import findlist, find

def shell_interactive():
    parser=ArgumentParser()

    parser.add_argument('-p','--path', dest='startdir',
                        help='find start from startdir(default os.curdir)')

    parser.add_argument('pattern', nargs='+',
                        help='such as *.c *.py')

    parser.add_argument('-e', '--exec', default=None,
                        help='exec other command by pipe like -exec "xxx yyy" ')

    parser.add_argument('-r', '--regex', action='store_true',
                        help='pattern regex match')


    args=parser.parse_args()

    return args.__dict__

def main():
    args=shell_interactive()
    import os
    if args['startdir']==None:
        args['startdir']=os.curdir

    if args['regex'] != None:
        regex = True
    else:
        regex = False

    if args['exec']!=None:

        exec_cmd = args['exec']

    import minghu6.etc.cmd as cmd

    for pattern in args['pattern']:

        for file in find(pattern,args['startdir'],regex_match=regex):
            pprint(file)
            if args['exec']!=None:
                pprint(exec_cmd + ' ' + file)
                lines = cmd.exec_cmd(exec_cmd + ' ' + file)[0]
                pprint(lines)

if __name__ == '__main__':
    main()