# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""ffmpeg_fix
A ffmpeg tools
Usage:
  ffmpeg_fix info <filename> [-l]
  ffmpeg_fix convert <filename> --output=<output> [--fps=<fps>] [--rate=<rate>]
                                                [--size=<size>]
  ffmpeg_fix merge <pattern>... --output=<output> [--prefix]
  ffmpeg_fix cut <filename> <start-time> <end-time> --output=<output>

Options:
  info                  view the info of the file.
  convert               convert the format of the file.
  cut                   cut the video.
  <pattern>             pattern of video name, such as "p_*" (p_1.mp4, p_2.mp4, p_3.mp4)
                        Only support name without path.
  <start-time>          video start time, 0 means 00:00:00
  <end-time>            video end time, such as xx:yy:zz, xxx:yy:zz
  -o --output=<output>  ouput file
  -l                    list all information
  --prefix              the pattern is file name prefix
  --fps=<fps>           change the video of FPS suach as "29.97"
  --rate=<rate>         video rate, such as 1.5, 2, 0.5 etc. (only video, exclude music!)
  --size=<size>         video size, such as "1080x720"

"""

from argparse import ArgumentParser
import os
import uuid
import re
import sqlite3
import csv
from collections import namedtuple
import json
from pprint import pprint
from contextlib import redirect_stdout
import io
import fnmatch
from distutils.version import LooseVersion
import decimal
context=decimal.getcontext() # 获取decimal现在的上下文
context.rounding = decimal.ROUND_05UP

from docopt import docopt

import minghu6
from minghu6.math.prime import simpleist_int_ratio
from minghu6.etc.cmd import exec_cmd, has_proper_ffmpeg
from minghu6.text.color import color
from minghu6.algs.var import each_same
from minghu6.etc.path2uuid import path2uuid
from minghu6.etc.path import add_postfix
from minghu6.io.stdio import askyesno


def test_ffmpeg():
    if not has_proper_ffmpeg():
        color.print_err('You need ffmpeg')
        return

LOGFILENAME='.videonamedict'
LogStruct=namedtuple('uuid_raw_dict', ['uuid_name', 'raw_name', 'target_name'])

def convert_video(i, video_format='.mp4', others=''):

    if not os.path.isfile(i):
        color.print_err('{0:s} is not a file'.format(i))
        return

    elif '.'+os.path.splitext(i)[1] == video_format:
        color.print_warn('skip the video file {0:s}'.format(i))
        return

    else:

        i_base = os.path.splitext(os.path.basename(i))[0]
        cmd = 'ffmpeg -i'

        out = i_base + video_format
        i_tmpfn = os.path.join(os.path.dirname(i),
                               uuid.uuid3(uuid.NAMESPACE_DNS,
                                          os.path.basename(i)).hex)

        i_tmpfn += os.path.splitext(i)[1]

        out_tmpfn = os.path.splitext(i_tmpfn)[0] + video_format

        with open(LOGFILENAME, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            row = LogStruct(uuid_name=i_tmpfn,
                             raw_name=i,
                             target_name=out_tmpfn)
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                from minghu6.text.encoding import get_locale_codec
                default_codec = get_locale_codec()
                codec = ({'utf8', 'gbk'} ^ {default_codec}).pop()
                raw_name = row.raw_name.encode(codec).decode(default_codec,
                                                             errors='ignore')
                target_name = row.target_name.encode(codec).decode(default_codec,
                                                                   errors='ignore')
                new_row = LogStruct(uuid_name=i_tmpfn,
                                    raw_name=raw_name,
                                    target_name=target_name)
                writer.writerow(new_row)

        try:
            os.rename(i, i_tmpfn)
        except FileExistsError as ex:
            color.print_warn(ex)

        cmd = ' '.join([cmd, i_tmpfn, ' '.join(others), out_tmpfn])
        color.print_info('start to convert the video {0:s} ...'.format(i_base))
        try:
            exec_cmd(cmd)
            #print(cmd)
        except Exception as ex:
            color.print_err(ex)
            color.print_err('video {0:s} convert failed.\n'.format(i_base))
        else:
            color.print_ok('video {0:s} convert sucessful.\n'.format(i_base))
            try:
                os.rename(out_tmpfn, out)
            except FileNotFoundError as ex:
                color.print_err(ex)
        finally:
            os.rename(i_tmpfn, i)
            os.remove(LOGFILENAME)


def convert_video_dir(dn, video_format='.mp4', others=''):

    if os.path.isdir(dn):
        for pat in ['*.f4v', '*.flv', '*.3gp']:
            for vn in find(pat, dn):
                convert_video(vn, video_format, others)


def main(i, video_format, others):

    if os.path.exists(LOGFILENAME):
        with open(LOGFILENAME, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in map(LogStruct._make, reader):
                if os.path.exists(row.uuid_name):
                    os.rename(row.uuid_name, row.raw_name)
                    os.remove(row.target_name)

        os.remove(LOGFILENAME)


    if os.path.isfile(i):
        convert_video(i, video_format, others)
    elif os.path.isdir(i):
        convert_video_dir(i, video_format, others)
    else:
        color.print_err('param i is neigher video file nor directory')


'''
def cli():
    test_ffmpeg()

    parser = ArgumentParser(description='An ffmpeg enHance tool',
                            epilog=('exp: ffmpeg_fix -i "abc ghi.flv" '
                                    '-f .mp4 "-b:v 640k"'))

    parser.add_argument('-i',
                        help='input video stream or directory')


    parser.add_argument('-f', '--format',dest='video_format',
                        help='output video format like .mp4')

    parser.add_argument(nargs='*', dest='others',
                        help='other params of ffmpeg')



    args = parser.parse_args().__dict__
    main(**args)
'''
def load_video_info_json(fn):
    cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams "%s" ' % fn
    info_lines, _ = exec_cmd(cmd)
    s = '\n'.join(info_lines)
    json_obj = json.loads(s)
    return json_obj

def load_fps_from_json(json_obj):
    """

    :param json_obj:
    :return: float
    """
    frame_rate = json_obj['streams'][0]['avg_frame_rate']
    fraction, denominator = frame_rate.split('/')
    frame_rate = int(fraction) / int(denominator)
    return frame_rate

def info(fn, list_all=False):

    json_obj = load_video_info_json(fn)

    if not list_all:
        filename = json_obj['format']['filename']

        size = json_obj['format']['size']

        bit_rate = json_obj['format']['bit_rate']
        frame_rate = load_fps_from_json(json_obj)

        width = json_obj['streams'][0]['width']
        height = json_obj['streams'][0]['height']
        resolution = '%sx%s'%(width, height)
        ratio_tuple = simpleist_int_ratio(width, height)

        format_name = json_obj['format']['format_name']
        format_long_name = json_obj['format']['format_long_name']

        codec_name = json_obj['streams'][0]['codec_name']
        codec_long_name = json_obj['streams'][0]['codec_long_name']

        tracks_codec_name = json_obj['streams'][1]['codec_name']
        tracks_channels = json_obj['streams'][1]['channels']


        color.print_info('filename:         %s'%filename)
        color.print_info('size:             %.1f Mb'%(int(size)/(1024*1024)))
        color.print_info('bit_rate:         %.2f Mb/s'%(int(bit_rate)/1000/1000))
        color.print_info('resolution:       %s'%resolution + ' (%s:%s)'%ratio_tuple)
        color.print_info('frame_rate:       %.2f fps'%frame_rate)
        color.print_info('format_name:      %s'%format_name)
        color.print_info('format_long_name: %s'%format_long_name)
        color.print_info('codec_name:       %s'%codec_name)
        color.print_info('codec_long_name:  %s'%codec_long_name)
        color.print_info()
        color.print_info('tracks_codec_name:%s'%tracks_codec_name)
        color.print_info('tracks_channels:  %s'%tracks_channels)

    else:

        buf = io.StringIO()
        with redirect_stdout(buf):
            pprint(json_obj)

        color.print_info(buf.getvalue())

def convert(fn, output, size:str=None, rate:(int, float)=None, fps:(int, float)=None):
    fn_tmp = path2uuid(fn, quiet=True)
    output_tmp = path2uuid(output, rename=False)
    try:
        json_obj = load_video_info_json(fn_tmp)
        color.print_info('start convert %s to %s'%(fn, output))
        cmd_list = ['ffmpeg', '-i', fn_tmp]
        need_convert = False
        if rate is not None and rate != 1:
            source_origin_fps = load_fps_from_json(json_obj)
            source_fps = source_origin_fps * float(rate)
            cmd_list.insert(1, '-r')
            cmd_list.insert(2, str(source_fps))
            need_convert = True

        if size is not None:
            width = json_obj['streams'][0]['width']
            height = json_obj['streams'][0]['height']
            origin_size = '%sx%s'%(width, height)
            if origin_size != size:
                color.print_info('convert size from %s to %s'%(origin_size,
                                                               size))
                cmd_list.append('-s')
                cmd_list.append(size)
                need_convert = True

        if fps is not None:
            origin_fps = round(load_fps_from_json(json_obj), 3)
            if round(fps, 3) != origin_fps:
                cmd_list.append('-r')
                cmd_list.append(str(fps))
                color.print_info('convert fps from %f to %f'%(origin_fps,
                                                               fps))
                need_convert = True

        _, ext_i = os.path.splitext(fn)
        _, ext_out = os.path.splitext(output)
        if ext_i != ext_out:
            need_convert = True

        if need_convert:
            cmd_list.append(output_tmp)
            exec_cmd(cmd_list)
        else:
            os.rename(fn_tmp, output_tmp)

        path2uuid(output_tmp, d=True)
    except Exception as ex:
        path2uuid(output_tmp, d=True, rename=False)
        raise
    finally:
        path2uuid(fn_tmp, d=True)

def merge(pattern_list, output, isprefix=False):

    if os.path.splitext(output)[1] == '':
        color.print_err('you are supposed to point to the output format explicitly!')
        color.print_err('Failed.')
        return
    base_dir = os.curdir
    merge_file_list = []
    merge_file_list2 = []
    for fn in os.listdir(base_dir):
        if os.path.isdir(fn):
            continue
        if fn == '.path2uuid.sqlite3':
            continue

        for pattern in pattern_list:
            if isprefix:
                if fn.lower().startswith(pattern.lower()):
                    merge_file_list.append(fn)
            else:
                if fnmatch.fnmatch(fn, pattern):
                    merge_file_list.append(fn)

    #common_prefix_pattern = r'^(\w)+\+$'
    if isprefix and len(pattern_list)==1:
        def key(fn):
            base = os.path.splitext(os.path.basename(fn))[0]
            v = LooseVersion(base.split(pattern_list[0])[1])
            return v
    else:
        key = lambda fn:fn

    merge_file_list = sorted(merge_file_list, key=key)

    color.print_info('The following video file will be merged in order')
    for i, file_to_merge in enumerate(merge_file_list):
        color.print_info('%3d. %s'%(i, file_to_merge))

    if len(merge_file_list) <= 1:
        color.print_info('Do nothing.')
        return
    args = input('press enter to continue, q to quit')
    if args in ('q', 'Q'):
        return

    # check if the video can be merge
    FileInfo = namedtuple('FileInfo', ['width', 'height', 'fps'])
    merge_file_info_list = []
    for fn in merge_file_list:
        json_obj = load_video_info_json(fn)

        codec_name = json_obj['streams'][0]['codec_name']
        width = int(json_obj['streams'][0]['width'])
        height = int(json_obj['streams'][0]['height'])
        fps = round(load_fps_from_json(json_obj), 3)

        merge_file_info_list.append(FileInfo(width, height, fps))

    merge_file_tmp_list = list(map(lambda x:path2uuid(x), merge_file_list))
    merge_file_tmp_list2 = []
    if not each_same(merge_file_info_list, key=lambda x:(x.width, x.height, x.fps)):
        color.print_err('width, height, fps should be same of all video')

        min_width = sorted(merge_file_info_list, key=lambda x:x.width)[0].width
        min_height = sorted(merge_file_info_list, key=lambda x:x.height)[0].height
        min_resolution = '%dx%d'%(min_width, min_height)
        min_fps = sorted(merge_file_info_list, key=lambda x:x.fps)[0].fps

        color.print_info('all_to_resolution: %s'%min_resolution)
        color.print_info('all_to_fps: %s'%min_fps)
        if askyesno('convert to fix?'):
            merge_file_tmp_list2 = list(map(lambda x:add_postfix(x, 'tmp'), merge_file_tmp_list))
            def tmp(fn_tuple):
                print(fn_tuple)
                convert(*fn_tuple, size=min_resolution, fps=min_fps)

            list(map(lambda x:tmp(x),
                zip(merge_file_tmp_list, merge_file_tmp_list2)))

        else:
            return

    output_tmp = path2uuid(output, rename=False, quiet=True)
    if len(merge_file_tmp_list2) == 0:
        input_file_list = merge_file_tmp_list
    else:
        input_file_list = merge_file_tmp_list2
    try:

        fw = open('.mylist', 'w')
        for fn in input_file_list:
            fw.write("file '%s' \n"%fn)

        fw.close()
        merge_cmd = 'ffmpeg -f concat -i %s -c copy %s'%('.mylist', output_tmp)
        exec_cmd(merge_cmd)

        path2uuid(output_tmp, d=True)
    except:
        raise
    else:
        color.print_ok('Done.')
    finally:
        try:
            os.remove('.mylist')
        except:
            pass

        for fn in input_file_list:
            path2uuid(fn, d=True)


def cut(fn, output, start_time, end_time):
    def video_time_str2int(s):
        s_list = reversed(s.split(':'))
        sec = 0
        for i, t in enumerate(s_list):
            sec += int(t) * 60**i
        return sec

    start_time_int = video_time_str2int(start_time)
    end_time_int = video_time_str2int(end_time)
    long = end_time_int - start_time_int
    if long <= 0:
        color.print_err('end-time:%s is before than start-time:%s'%(end_time, start_time))
        return
    fn_tmp = path2uuid(fn)
    output_tmp = path2uuid(output, rename=False)
    try:
        cmd = 'ffmpeg -ss %d -i "%s" -t %d -c:v copy -c:a copy "%s" '\
              %(start_time_int, fn_tmp, long, output)

        exec_cmd(cmd)
        path2uuid(output_tmp, d=True, rename=False)
    except:
        raise
    else:
        color.print_ok('cut the video %s to %s from %s to %s'
                       %(fn, output, start_time, end_time))

    finally:
        path2uuid(fn_tmp, d=True)

def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    if arguments['info']:
        fn = arguments['<filename>']
        list_all = arguments['-l']
        info(fn, list_all)
    elif arguments['convert']:
        fn = arguments['<filename>']
        output = arguments['--output']
        if arguments['--fps'] is not None:
            fps = float(arguments['--fps'])
        else:
            fps = None

        if arguments['--rate'] is not None:
            rate = float(arguments['--rate'])
        else:
            rate = None

        size = arguments['--size']

        convert(fn, output, size=size, rate=rate, fps=fps)

    elif arguments['merge']:
        pattern= arguments['<pattern>']
        output = arguments['--output']
        isprefix = arguments['--prefix']
        merge(pattern, output, isprefix)

    elif arguments['cut']:
        fn = arguments['<filename>']
        start_time = arguments['<start-time>']
        end_time = arguments['<end-time>']
        output = arguments['--output']

        cut(fn, output, start_time, end_time)





if __name__ == '__main__':

    cli()