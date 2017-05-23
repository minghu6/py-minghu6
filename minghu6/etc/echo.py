import sys

from minghu6.algs.operator import getitem

__all__ = ['echo']


def echo(s):
    # sys.stdout.write(s)
    print(s)


if __name__ == '__main__':
    echo(getitem(sys.argv, 1, ''))
