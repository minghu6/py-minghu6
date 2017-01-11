# -*- coding:utf-8 -*-
#!/usr/bin/env python3
"""
Tail


Usage:
  tail <filename> [-n=<n>] [--encoding=<encoding>]

Options:
  -n=<n>                 head number of the file [default: 5].
  --encoding=<encoding>  point the encoding of the file manually

"""
from docopt import docopt
import cchardet as chardet
import os
import minghu6
from minghu6.etc import fileecho
from minghu6.text.color import color

def main(path, n, encoding=None):
    try:
        with open(path, 'rb') as f:
            res_list = fileecho.tail(f, n)
            res = b'\n'.join(res_list)
            detect_result=chardet.detect(res)

            if encoding != None:
                codec = encoding
            elif detect_result['confidence'] > 0.7:
                codec = detect_result['encoding']
            else:
                color.print_warn('Not Known encoding, may be %s.\n'
                                'Please point it explictly'%detect_result['encoding'])
                return

            color.print_info(res.decode(codec, errors='ignore'))

    except FileNotFoundError:
        color.print_err('%s not found'%path)


def interavtive():
    arguments = docopt(__doc__, version=minghu6.__version__)

    n = int(arguments['-n'])
    encoding = arguments['--encoding']
    path = arguments['<filename>']

    main(path, n, encoding=encoding)
    #color.print_info(arguments)

if __name__ == '__main__':
    interavtive()