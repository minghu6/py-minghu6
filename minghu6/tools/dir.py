# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
dir all tools in minghu6.tools
"""
import os
from importlib import import_module
from color import color


def is_tool_module(module_name):
    if module_name.find('__init__') != -1:
        return False
    elif module_name.find('unitest') != -1:
        return False
    elif module_name.startswith(('.', '_')):
        return False
    else:
        return True


def show_doc(name: str):
    m = import_module('minghu6.tools.' + name)

    return m.__doc__


def cli():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('given_name', metavar='module_name', nargs='*',
                        help='list doc of the specified module')

    parser.add_argument('-l', action='store_true',
                        help='show all module doc')

    args = parser.parse_args().__dict__

    given_name = args.get('given_name', ())
    l = args.get('l', False)

    curpath = os.path.dirname(__file__)

    for i, fn in enumerate(os.listdir(curpath)):
        if fn.endswith('.py'):
            module_name = fn[:-3]
        # check if it's a folder module
        elif not os.path.isdir(os.path.join(curpath, fn)):
            continue
        else:
            module_name = fn

        if is_tool_module(module_name):
            if len(given_name) == 0 and not l:  # list all module in short
                print('{0:2d} {1:s}'.format(i + 1, module_name))
            elif len(given_name) != 0:  # list someone module (detailed)
                if module_name in given_name:
                    print(module_name, show_doc(module_name))
            elif l:  # list all module in detail
                color.print_dark_green(i + 1, module_name)
                color.print_white(show_doc(module_name))
                print()
                print()


def term_interactive():
    from simple_term_menu import TerminalMenu

    curpath = os.path.dirname(__file__)
    module_names = []

    for fn in os.listdir(curpath):
        if fn.endswith('.py'):
            module_name = fn[:-3]
        # check if it's a folder module
        elif not os.path.isdir(os.path.join(curpath, fn)):
            continue
        else:
            module_name = fn

        if is_tool_module(module_name):
            module_names.append(module_name)

    module_names.remove('cjg')

    module_menu = TerminalMenu(
        module_names,
        # ["abc", "def", "ghi"],
        menu_highlight_style=('bg_green', 'bold', 'underline'),
        title='Modules',
        cycle_cursor=True,
        raise_error_on_interrupt=True,
        preview_command=show_doc,
        preview_size = 0.75
    )

    module_menu.show()


if __name__ == '__main__':
    term_interactive()
