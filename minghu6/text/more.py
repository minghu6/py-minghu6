# -*-coding:UTF-8-*-
# for python 3.x
"""
分页显示
"""
from color import color

__all__ = ['more']


def more(text, numlines=40, print_color=False):
    lines = text.splitlines()
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk:
            if print_color:
                color.print_info(line)
            else:
                print(line)

        if not lines: break
        if print_color:
            color.printDarkPink('More?')
        else:
            print('More?', end='')
        if lines and input().upper() in ('N', 'NO', 'Q', 'QUIET'):
            break


if __name__ == '__main__':
    import sys

    more(open(sys.argv[1]).read(), 10)
