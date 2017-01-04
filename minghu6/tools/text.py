# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""Text

Usage:
  text charset <filename>
  text convert <filename> <to_charset> [--from_charset=<from_charset>] [--output=<output>]
  text merge   <filename>... --output=<output>
  text merge   --regex=<regular-expression> --output=<output>

Options:
  charset                          look up the encoding of the file
  <to_encoding>                    target charset
  -o --output=<output>             don't write back, give a output path
  -r --regex=<regular-expression>  specific files by a regular expression

"""
from docopt import docopt
import chardet
import os
import tempfile
import shutil
import minghu6
from minghu6.etc import fileecho
from minghu6.text.color import color
from minghu6.etc.find import findlist

def interactive():
    arguments = docopt(__doc__, version=minghu6.__version__)

    path_list = arguments['<filename>']
    try:
        fr_list=[]
        [fr_list.append(open(path, 'rb')) for path in path_list]

    except FileNotFoundError:
        color.print_err('%s not found'%path_list)
        return
    else:

        if arguments['charset']:
            fr = fr_list[0]
            encoding, confidence = fileecho.guess_charset(fr)
            if encoding == None:
                color.print_err('unknown')
            else:
                color.print_info(encoding, confidence)

            fr.close()

        elif arguments['convert']:
            fr = fr_list[0]
            path = path_list[0]
            to_charset = arguments['<to_charset>']
            from_charset = arguments['--from_charset']
            if from_charset == None:
                encoding, confidence = fileecho.guess_charset(fr)
                if confidence == None:
                    color.print_err('unknown from_charset, '
                                    'you must point it explicity')
                    return
                elif confidence < 0.7:
                    color.print_warn('uncertained from_charset, '
                                     'maybe %s\n'
                                     'you must point it explicity'%encoding)
                    return
                else:
                    from_charset = encoding

                    # rename(name_old, name_new)
                    # name_a, name_b must same driver in windows
                    dir = os.path.dirname(os.path.abspath(path))
                    fwn = tempfile.mktemp(dir=dir)
                    with open(fwn, 'wb') as fw:
                        for line in fr:
                            fw.write(line.decode(from_charset, errors='ignore')
                                         .encode(to_charset, errors='ignore'))

                    fr.close()
                    if arguments['--output'] == None:
                        shutil.copy(fwn, path)
                    else:
                        shutil.copy(fwn, arguments['--output'])

                    os.remove(fwn)

        elif arguments['merge']:
            if arguments['--regex'] !=None :
                #color.print_info(arguments)
                merge_file_path_list = findlist(startdir=os.curdir,
                                           pattern=arguments['--regex'],
                                           regex_match=True, dosort=True)

            else:
                merge_file_path_list = arguments['<filename>']

            with open(arguments['--output'], 'wb') as outfile:
                for infile_path in merge_file_path_list:
                    with open(infile_path, 'rb') as infile:
                        outfile.write(infile.read())

                    outfile.write(b'\n')
                    color.print_ok('have merged file %s'%infile_path)





if __name__ == '__main__':
    interactive()