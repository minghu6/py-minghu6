# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
dir all tools in minghu6.tools
"""
import os



from importlib import import_module
from minghu6.etc.find import find
from minghu6.text.color import color

def main(given_name=(), l=False):
    curpath = os.path.dirname(__file__)
    #print(curpath)
    def is_tool_module(module_name):
        if module_name.find('__init__') != -1:
            return False
        elif module_name.find('unitest') != -1:
            return False

        else:
            return True


    for i, fn in enumerate(find('*.py', curpath)):

        module_name =fn[len(curpath)+1:-3]
        if is_tool_module(module_name):

            if len(given_name) == 0 and not l:
                print('{0:2d} {1:s}'.format(i+1, module_name))

            elif len(given_name) != 0:
                if module_name in given_name:
                    m = import_module('minghu6.tools.'+module_name)
                    print(module_name, m.__doc__)

            elif l:
                    m = import_module('minghu6.tools.'+module_name)
                    color.printDarkGreen(i+1, module_name)
                    color.printWhite(m.__doc__)
                    print()
                    print()



def interactive():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('given_name', metavar='module_name', nargs='*',
                        help='list doc of the specified module')

    parser.add_argument('-l', action='store_true',
                        help='show all module doc')

    args = parser.parse_args().__dict__
    #print(args)
    main(**args)

if __name__ == '__main__':

    interactive()