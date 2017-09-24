# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""ffmpeg_fix
A ffmpeg tools
Usage:
  ffmpeg_fix info <filename> [-l]
  ffmpeg_fix convert <filename> --output=<output> [--fps=<fps>] [--rate=<rate>]
                                                  [--size=<size>]
  ffmpeg_fix convert <filename> --format=<format> [--fps=<fps>] [--rate=<rate>]
                                            [--size=<size>]
  ffmpeg_fix merge audio <pattern>... --output=<output> [--prefix]
  ffmpeg_fix merge vedio <pattern>... --output=<output> [--prefix]
  ffmpeg_fix merge va    <vedioname> <audioname> --output=<output>
  ffmpeg_fix merge vs    <vedioname> <subtitlename> --output=<output>
  ffmpeg_fix merge gif   <pattern>   --framerate=<framerate> --output=<output> [--prefix]
  ffmpeg_fix cut <filename> <start-time> <end-time> --output=<output> [--debug]
  ffmpeg_fix extract audio <filename> --output=<output>
  ffmpeg_fix extract vedio <filename> --output=<output>
  ffmpeg_fix extract subtitle <filename> --output=<output>
  ffmpeg_fix extract frame <filename> <start-time> --output=<output>

Options:
  info                  view the info of the file.
  convert               convert the format of the file(video, music).
  cut                   cut the video.
  extract-audio         extract tracks from video
  va                    video and audio
  vs                    video and subtitle
  <pattern>             pattern of video name, such as "p_*" (p_1.mp4, p_2.mp4, p_3.mp4)
                        Only support name without path.
  <start-time>          video start time, 0 means 00:00:00
  <end-time>            video end time, such as xx:yy:zz, xxx:yy:zz

  -f --format=<format>  to format such as `mp4`
  -o --output=<output>  ouput file
  -l                    list all information
  --prefix              the pattern is file name prefix
  --fps=<fps>           change the video of FPS suach as "29.97"
  --rate=<rate>         video rate, such as 1.5, 2, 0.5 etc. (only video, exclude music!)
  --size=<size>         video size, such as "1080x720"

"""

import decimal
import fnmatch
import json
import os
import sys
from collections import namedtuple
from contextlib import redirect_stdout
from distutils.version import LooseVersion

import io
from pprint import pprint

context = decimal.getcontext()  # 获取decimal现在的上下文
context.rounding = decimal.ROUND_05UP

from docopt import docopt

import minghu6
from minghu6.math.prime import simpleist_int_ratio
from minghu6.etc.cmd import exec_cmd
from color import color
from minghu6.algs.var import each_same
from minghu6.etc.path2uuid import path2uuid
from minghu6.etc.path import add_postfix
from minghu6.etc.fileecho import guess_charset
from minghu6.io.stdio import askyesno


def assert_output_has_ext(fn):
    if os.path.splitext(fn)[1] == '':
        color.print_err('you are supposed to point to the output format explicitly!')
        return False
    else:
        return True


def video_time_str2int(s):
    s_list = reversed(s.split(':'))
    sec = 0
    for i, t in enumerate(s_list):
        sec += int(t) * 60 ** i
    return sec


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
    video_site, audio_site = get_video_audio_info_site_injson(json_obj)
    frame_rate = json_obj['streams'][video_site]['avg_frame_rate']
    fraction, denominator = frame_rate.split('/')
    frame_rate = int(fraction) / int(denominator)

    return frame_rate


def get_video_audio_info_site_injson(json_obj):
    for i, stream in enumerate(json_obj['streams']):
        if 'channels' in stream:
            audio_site = i
        if stream['avg_frame_rate'] != '0/0':
            vedio_site = i

    return vedio_site, audio_site


def info(fn, list_all=False):
    json_obj = load_video_info_json(fn)

    if not list_all:
        def video_info(json_obj):
            video_site, audio_site = get_video_audio_info_site_injson(json_obj)
            filename = json_obj['format']['filename']

            size = json_obj['format']['size']

            bit_rate = json_obj['format']['bit_rate']
            frame_rate = load_fps_from_json(json_obj)

            width = json_obj['streams'][video_site]['width']
            height = json_obj['streams'][video_site]['height']
            resolution = '%sx%s' % (width, height)
            ratio_tuple = simpleist_int_ratio(width, height)

            format_name = json_obj['format']['format_name']
            format_long_name = json_obj['format']['format_long_name']

            codec_name = json_obj['streams'][video_site]['codec_name']
            codec_long_name = json_obj['streams'][video_site]['codec_long_name']

            audio_codec_name = json_obj['streams'][audio_site]['codec_name']
            audio_tag_string = json_obj['streams'][audio_site]['codec_tag_string']
            audio_channels = json_obj['streams'][audio_site]['channels']

            color.print_info('filename:         %s' % filename)
            color.print_info('size:             %.1f Mb' % (int(size) / (1024 * 1024)))
            color.print_info('bit_rate:         %.2f Mb/s' % (int(bit_rate) / 1000 / 1000))
            color.print_info('resolution:       %s' % resolution + ' (%s:%s)' % ratio_tuple)
            color.print_info('frame_rate:       %.2f fps' % frame_rate)
            color.print_info('format_name:      %s' % format_name)
            color.print_info('format_long_name: %s' % format_long_name)
            color.print_info('codec_name:       %s' % codec_name)
            color.print_info('codec_long_name:  %s' % codec_long_name)
            color.print_info()
            color.print_info('audio_codec_name: %s' % audio_codec_name)
            color.print_info('audio_tag_string: %s' % audio_tag_string)
            color.print_info('audio_channels:   %s' % audio_channels)

        def audio_info(json_obj):
            video_site, audio_site = get_video_audio_info_site_injson(json_obj)

            filename = json_obj['format']['filename']
            size = json_obj['format']['size']

            format_name = json_obj['format']['format_name']
            format_long_name = json_obj['format']['format_long_name']

            codec_name = json_obj['streams'][audio_site]['codec_name']
            codec_long_name = json_obj['streams'][audio_site]['codec_long_name']

            bit_rate = json_obj['streams'][audio_site]['bit_rate']
            sample_rate = json_obj['streams'][audio_site]['sample_rate']

            color.print_info('filename:         %s' % filename)
            color.print_info('size:             %.1f Mb' % (int(size) / (1024 * 1024)))
            color.print_info('bit_rate:         %d Kb/s' % (int(bit_rate) / 1000))
            color.print_info('sample_rate:      %.1f KHz' % (int(sample_rate) / 1000))
            color.print_info('format_name:      %s' % format_name)
            color.print_info('format_long_name: %s' % format_long_name)
            color.print_info('codec_name:       %s' % codec_name)
            color.print_info('codec_long_name:  %s' % codec_long_name)

        try:
            video_info(json_obj)
        except:
            audio_info(json_obj)


    else:

        buf = io.StringIO()
        with redirect_stdout(buf):
            pprint(json_obj)

        color.print_info(buf.getvalue())


def convert(fn, output, size: str = None, rate: (int, float) = None, fps: (int, float) = None):
    if not assert_output_has_ext(output):
        color.print_err('Failed.')
        return

    fn_tmp = path2uuid(fn, quiet=True)
    output_tmp = path2uuid(output, quiet=True, rename=False)
    try:
        json_obj = load_video_info_json(fn_tmp)
        video_site, audio_site = get_video_audio_info_site_injson(json_obj)
        color.print_info('start convert %s to %s' % (fn, output))
        cmd_list = ['ffmpeg', '-i', fn_tmp]
        need_convert = False
        if rate is not None and rate != 1:
            source_origin_fps = load_fps_from_json(json_obj)
            source_fps = source_origin_fps * float(rate)
            cmd_list.insert(1, '-r')
            cmd_list.insert(2, str(source_fps))
            need_convert = True

        if size is not None:
            width = json_obj['streams'][video_site]['width']
            height = json_obj['streams'][video_site]['height']
            origin_size = '%sx%s' % (width, height)
            if origin_size != size:
                color.print_info('convert size from %s to %s' % (origin_size,
                                                                 size))
                cmd_list.append('-s')
                cmd_list.append(size)
                need_convert = True

        if fps is not None:
            origin_fps = round(load_fps_from_json(json_obj), 3)
            if round(fps, 3) != origin_fps:
                cmd_list.append('-r')
                cmd_list.append(str(fps))
                color.print_info('convert fps from %f to %f' % (origin_fps,
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


def merge(pattern_list, output, type, **other_kwargs):
    isprefix = other_kwargs.get('isprefix', False)
    if not assert_output_has_ext(output):
        color.print_err('Failed.')
        return
    base_dir = os.curdir
    merge_file_list = []
    merge_file_list2 = []
    if type in ('vedio', 'audio', 'gif'):
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
    else:  # 'va', 'vs
        merge_file_list = pattern_list

    # common_prefix_pattern = r'^(\w)+\+$'
    if isprefix and len(pattern_list) == 1:
        def key(fn):
            base = os.path.splitext(os.path.basename(fn))[0]
            v = LooseVersion(base.split(pattern_list[0])[1])
            return v
    elif type in ('va', 'vs'):
        key = lambda x: 0
    else:
        key = lambda fn: fn

    merge_file_list = sorted(merge_file_list, key=key)

    color.print_info('The following file will be merged in order')
    for i, file_to_merge in enumerate(merge_file_list):
        color.print_info('%3d. %s' % (i, file_to_merge))

    if len(merge_file_list) <= 1:
        color.print_info('Do nothing.')
        return
    args = input('press enter to continue, q to quit')
    if args in ('q', 'Q'):
        return

    merge_file_tmp_list = list(map(lambda x: path2uuid(x, quiet=True), merge_file_list))
    merge_file_tmp_list2 = []

    if type == 'vedio':
        # check if the video can be merge
        FileInfo = namedtuple('FileInfo', ['width', 'height', 'fps'])
        merge_file_info_list = []
        for fn in merge_file_tmp_list:
            json_obj = load_video_info_json(fn)
            video_site, audio_site = get_video_audio_info_site_injson(json_obj)
            codec_name = json_obj['streams'][video_site]['codec_name']
            width = int(json_obj['streams'][video_site]['width'])
            height = int(json_obj['streams'][video_site]['height'])
            fps = round(load_fps_from_json(json_obj), 3)

            merge_file_info_list.append(FileInfo(width, height, fps))

        if not each_same(merge_file_info_list, key=lambda x: (x.width, x.height, x.fps)):
            color.print_err('width, height, fps should be same of all video')

            min_width = sorted(merge_file_info_list, key=lambda x: x.width)[0].width
            min_height = sorted(merge_file_info_list, key=lambda x: x.height)[0].height
            min_resolution = '%dx%d' % (min_width, min_height)
            min_fps = sorted(merge_file_info_list, key=lambda x: x.fps)[0].fps

            color.print_warn('all_to_resolution: %s' % min_resolution)
            color.print_warn('all_to_fps: %s' % min_fps)
            if askyesno('convert to fix?'):
                merge_file_tmp_list2 = list(map(lambda x: add_postfix(x, 'tmp'), merge_file_tmp_list))

                def tmp(fn_tuple):
                    convert(*fn_tuple, size=min_resolution, fps=min_fps)

                list(map(lambda x: tmp(x),
                         zip(merge_file_tmp_list, merge_file_tmp_list2)))

            else:
                return

    elif type == 'audio':
        pass
    elif type == 'va':
        pass
    elif type == 'gif':
        pass

    output_tmp = path2uuid(output, rename=False, quiet=True)
    if len(merge_file_tmp_list2) == 0:
        input_file_list = merge_file_tmp_list
    else:
        input_file_list = merge_file_tmp_list2  # only for merge vedio
    try:

        fw = open('.mylist', 'w')
        for fn in input_file_list:
            fw.write("file '%s' \n" % fn)

        fw.close()
        if type in ('vedio', 'audio'):
            merge_cmd = 'ffmpeg -f concat -i %s -c copy %s' % ('.mylist', output_tmp)
        elif type == 'va':
            merge_cmd = 'ffmpeg -i %s -i %s -vcodec copy -acodec copy %s ' \
                        % (input_file_list[0], input_file_list[1], output_tmp)

        elif type == 'vs':
            with open(input_file_list[1]) as f_subtitle:
                encoding = guess_charset(f_subtitle)['encoding']

            if encoding.lower() not in ('utf-8', 'ascii'):
                info, err = exec_cmd('%s -m minghu6.tools.text convert %s utf-8'
                                     % (sys.executable, input_file_list[1]))

                if len(err) > 1 or err[0] != '':  # exec failed
                    color.print_err('error codec of the subtitle %s (need utf-8)')

            merge_cmd = 'ffmpeg -i %s -vf subtitles=%s %s' \
                        % (input_file_list[0], input_file_list[1], output_tmp)

        elif type == 'gif':
            framerate = other_kwargs['framerate']
            merge_cmd = 'ffmpeg -f image2 -framerate %d -i %s %s' \
                        % (int(framerate), '.mylist', output_tmp)

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


def cut(fn, output, start_time, end_time, debug=False):
    if not assert_output_has_ext(output):
        color.print_err('Failed.')
        return

    start_time_int = video_time_str2int(start_time)
    end_time_int = video_time_str2int(end_time)
    long = end_time_int - start_time_int
    if long <= 0:
        color.print_err('end-time:%s is before than start-time:%s' % (end_time, start_time))
        return
    fn_tmp = path2uuid(fn)
    output_tmp = path2uuid(output, rename=False, quiet=True)
    try:
        cmd = 'ffmpeg -ss %d -i "%s" -t %d -c:v copy -c:a copy "%s" ' \
              % (start_time_int, fn_tmp, long, output)

        info_lines, err_lines = exec_cmd(cmd)
        if debug:
            print(cmd)
            print('Info: %s' % '\n'.join(err_lines))

        path2uuid(output_tmp, d=True, rename=False)
    except:
        raise
    else:
        color.print_ok('cut the video %s to %s from %s to %s'
                       % (fn, output, start_time, end_time))

    finally:
        path2uuid(fn_tmp, d=True)


def extract(fn, output, type, **other_kwargs):
    if not assert_output_has_ext(output):
        color.print_err('Failed.')
        return
    fn_tmp = path2uuid(fn, quiet=True)
    output_tmp = path2uuid(output, quiet=True, rename=False)

    extract_cmd_list = ['ffmpeg', '-i', fn_tmp]
    if type == 'audio':
        extract_cmd_list.extend(['-acodec', 'copy', '-vn', output_tmp])
    elif type == 'vedio':
        extract_cmd_list.extend(['-vcodec', 'copy', '-an', output_tmp])
    elif type == 'subtitle':
        extract_cmd_list.extend(['-scodec', 'copy', '-an', '-vn', output_tmp])
    elif type == 'frame':
        start_time = video_time_str2int(other_kwargs['start-time'])
        extract_cmd_list.extend(['-y', '-f', 'image2', '-ss', str(start_time),
                                 '-vframes', '1', output_tmp])
    else:
        color.print_err('error type: %s' % type)
        return
    # print(extract_cmd_list)
    exec_cmd(extract_cmd_list)

    path2uuid(fn_tmp, d=True)
    try:
        path2uuid(output_tmp, d=True)
    except:
        path2uuid(output_tmp, d=True, rename=True)
        color.print_err('extract Failed.')
    else:
        color.print_ok('extract Done.')


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)

    if arguments['info']:
        fn = arguments['<filename>']
        list_all = arguments['-l']
        info(fn, list_all)
    elif arguments['convert']:
        fn = arguments['<filename>']
        if arguments['--output']:
            output = arguments['--output']
        else:  # f
            f = arguments['--format']
            output = os.path.splitext(f)[0] + '.' + f

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

        output = arguments['--output']
        isprefix = arguments['--prefix']
        other_kwargs = {'isprefix': isprefix}
        type = None
        pattern = None
        if arguments['audio']:
            type = 'audio'
            pattern = arguments['<pattern>']
        elif arguments['vedio']:
            type = 'vedio'
            pattern = arguments['<pattern>']
        elif arguments['va']:
            type = 'va'
            pattern = [arguments['<vedioname>'], arguments['<audioname>']]
        elif arguments['vs']:
            type = 'vs'
            pattern = [arguments['<vedioname>'], arguments['<subtitlename>']]

        elif arguments['gif']:
            type = 'gif'
            pattern = arguments['<pattern>']
            frame_rate = arguments['--framerate']
            other_kwargs['framerate'] = frame_rate

        merge(pattern, output, type, **other_kwargs)

    elif arguments['cut']:
        fn = arguments['<filename>']
        start_time = arguments['<start-time>']
        end_time = arguments['<end-time>']
        output = arguments['--output']
        debug = arguments['--debug']
        cut(fn, output, start_time, end_time, debug)

    elif arguments['extract']:
        fn = arguments['<filename>']
        output = arguments['--output']
        type = None
        other_kwargs = {}
        if arguments['audio']:
            type = 'audio'
        elif arguments['vedio']:
            type = 'vedio'
        elif arguments['subtitle']:
            type = 'subtitle'
        elif arguments['frame']:
            type = 'frame'
            other_kwargs['start-time'] = arguments['<start-time>']

        extract(fn, output, type, **other_kwargs)


if __name__ == '__main__':
    cli()
