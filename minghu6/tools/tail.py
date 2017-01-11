# -*- coding:utf-8 -*-
#!/usr/bin/env python3
"""
Tail


Usage:
  tail <filename> [-n=<n>] [--encoding=<encoding>] [--no-more]

Options:
  -n=<n>                 head number of the file [default: 5].
  --encoding=<encoding>  point the encoding of the file manually
  --no-more              don't use `more` to show

"""
from docopt import docopt
import cchardet as chardet
import minghu6
from minghu6.etc import fileecho
from minghu6.text.color import color
from minghu6.text.more import more

def main(path, n, encoding=None, no_more=False):
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

            if no_more:
                color.print_info(res.decode(codec, errors='ignore'))
            else:
                more(res.decode(codec, errors='ignore'), print_color=True)


    except FileNotFoundError:
        color.print_err('%s not found'%path)


def interavtive():
    arguments = docopt(__doc__, version=minghu6.__version__)

    n = int(arguments['-n'])
    encoding = arguments['--encoding']
    path = arguments['<filename>']

    no_more = arguments['--no-more']
    main(path, n, encoding=encoding, no_more=no_more)
    #color.print_info(arguments)

if __name__ == '__main__':
    interavtive()