# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""Text

Usage:
  text charset <filename>
  text convert <filename> <to_charset> [-d] [-i=<info>] [--FC=<from_charset>] [--output=<output>]
  text merge   <filename>... --output=<output>
  text merge   --regex=<regular-expression> --output=<output>

Options:
  charset                          look up the encoding of the file
  <to_encoding>                    target charset
  -o --output=<output>             don't write back, give a output path
  -r --regex=<regular-expression>  specific files by a regular expression
  -i=<info>                        filter text path
  -d                               is_dir

"""
import fnmatch
import os
from pprint import pprint

import minghu6
from docopt import docopt
from minghu6.etc import fileecho
from minghu6.etc.find import findlist
from color import color


def convert_file(fn, output, from_charset, to_charset):
    fr = open(fn, 'rb')
    
    if from_charset is None:
        result = fileecho.guess_charset(fr)
        if result is None:
            color.print_err(f"detect {fn} codec failed")
            return

        encoding, confidence = result['encoding'], result['confidence']
        if confidence is None:
            color.print_err('unknown from_charset, '
                            'you must point it explicit')
            return
        elif confidence < 0.7:
            color.print_warn('uncertain from_charset, '
                             'maybe %s\n'
                             'you must point it explicit' % encoding)
            return
        else:
            # color.print_bold("detect from_charset: %s" % from_charset)
            from_charset = encoding

    color.print_bold(f"-> {fn}: {from_charset} >>> {to_charset}")

    lines = [line.decode(from_charset).encode(to_charset) for line in fr]
    fr.close()

    # fn maybe same with output
    with open(output, 'wb') as fw:
        fw.writelines(lines)


def path_list_to_readers(path_list):
    fr_list = []

    try:
        [fr_list.append(open(path, 'rb')) for path in path_list]
    except FileNotFoundError:
        color.print_err('%s not found' % path_list)
        return

    return fr_list


def find(pats, start_dir):
    for (thisDir, subsHere, filesHere) in os.walk(start_dir):
        for name in filesHere:
            match_success = False
            for each_pat in pats:
                if fnmatch.fnmatch(name, each_pat):
                    match_success = True
                    break

            if match_success:
                fullpath = os.path.join(thisDir, name)
                yield fullpath


def read_lntxt(path):
    with open(path, 'r') as fr:
        return list(filter(lambda ln: len(ln), map(lambda ln: ln.strip(), fr.readlines())))


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    path_list = arguments['<filename>']

    if arguments['charset']:
        fr_list = path_list_to_readers(path_list)
        fr = fr_list[0]
        result = fileecho.guess_charset(fr)

        encoding, confidence = result['encoding'], result['confidence']
        if encoding is None:
            color.print_err('unknown')
        else:
            color.print_bold('{0}, {1:.2f}'.format(encoding, confidence))

        fr.close()

    elif arguments['convert']:
        fn = path_list[0]
        output = arguments['--output']
        to_charset = arguments['<to_charset>']
        from_charset = arguments['--FC']
        info = arguments['-i']
        is_dir = arguments['-d']

        if is_dir:
            # backup dir
            from shutil import copytree
            bk_path = os.path.join(os.path.dirname(fn), os.path.basename(fn) + ".bk")
            copytree(fn, bk_path)

            if info is None:
                pats = ['*']
            else:
                pats = read_lntxt(info)

            for sub_fn in find(pats, fn):
                convert_file(sub_fn, sub_fn, from_charset, to_charset)
        else:
            if output is None:
                output = fn
            convert_file(fn, output, from_charset, to_charset)

    elif arguments['merge']:
        if arguments['--regex'] is not None:
            print(arguments['--regex'])
            # color.print_bold(arguments)
            merge_file_path_list = findlist(startdir=os.curdir,
                                            pattern=arguments['--regex'],
                                            regex_match=True, dosort=True)
            color.print_normal('merge file:')
            pprint(merge_file_path_list)

        else:
            merge_file_path_list = arguments['<filename>']

        with open(arguments['--output'], 'wb') as outfile:
            for infile_path in merge_file_path_list:
                with open(infile_path, 'rb') as infile:
                    outfile.write(infile.read())

                outfile.write(b'\n')
                color.print_ok('have merged file %s' % infile_path)


if __name__ == '__main__':
    cli()
