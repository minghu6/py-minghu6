
import sys
from minghu6.algs.operator import getitem
def echo(s):
    sys.stdout.write(s)

if __name__ == '__main__':

    echo(getitem(sys.argv, 1, ''))
