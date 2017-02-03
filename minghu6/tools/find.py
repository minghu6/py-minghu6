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
    if args['startdir'] is None:
        args['startdir']=os.curdir

    if args['exec'] is not None:

        exec_cmd = args['exec']

    import minghu6.etc.cmd as cmd
    for file in find(args['pattern'], args['startdir'], regex_match=args['regex']):
        pprint(file)
        if args['exec'] is not None:
            pprint(exec_cmd + ' ' + file)
            lines = cmd.exec_cmd(exec_cmd + ' ' + file)[0]
            pprint(lines)

def cli():
    main()

if __name__ == '__main__':
    main()