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


    args=parser.parse_args()

    return args.__dict__

def main():
    args=shell_interactive()
    import os
    if args['startdir']==None:
        args['startdir']=os.curdir

    def format_execstr(s):
        '''
        >>> format_execstr('python3_-m_minghu6.tools.converCharset_--from_aa_--to_bb_--Char\\_set_c')
        python3 -m minghu6.tools.converCharset --from aa --to bb --Char_set c
        :param s:
        :return:
        '''
        l=[]
        ss=[]
        for c in s:
            if c=='\\':
                l.append(c)
            else:
                [ss.append('\\') for i in range(len(l)//2)]
                if c=='_':
                    if len(l)%2!=0:# is escaped char
                        ss.append('_')
                    else:
                        ss.append(' ')

                    l.clear()

                else:
                    ss.append(c)

        return ''.join(ss)

    if args['exec']!=None:

        #exec_cmd = format_execstr(args['exec'])
        exec_cmd = args['exec']
        #pprint(exec_cmd)

    import minghu6.etc.cmd as cmd

    for pattern in args['pattern']:

        for file in find(pattern,args['startdir']):
            pprint(file)
            if args['exec']!=None:
                pprint(exec_cmd + ' ' + file)
                lines = cmd.exec_cmd(exec_cmd + ' ' + file)[0]
                pprint(lines)

if __name__ == '__main__':
    main()