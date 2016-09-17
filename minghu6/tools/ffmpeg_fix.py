# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
 fix poor support about UNICODE filename and hard to use of ffmpeg
"""

from argparse import ArgumentParser
import os
import uuid

from minghu6.etc.cmd import exec_cmd
from minghu6.text.color import color
from minghu6.etc.find import find

def test_ffmpeg():
    assert exec_cmd('ffmpeg -version').__len__() != 0,  'You need ffmpeg'

def convert_video(i, video_format='.mp4', others=''):

    if not os.path.isfile(i):
        color.print_warn('skip the video {0:s}'.format(os.path.splitext(i)[0]))
        return

    elif os.path.exists(os.path.splitext(i)[0] + video_format):
        color.print_warn('skip the video {0:s}'.format(os.path.splitext(i)[0]))
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


def convert_video_dir(dn, video_format='.mp4', others=''):

    if os.path.isdir(dn):
        for pat in ['*.f4v', '*.flv', '*.3gp']:
            for vn in find(pat, dn):
                convert_video(vn, video_format, others)


def main(i, video_format, others):

    #print(i)
    if os.path.isfile(i):
        convert_video(i, video_format, others)
    elif os.path.isdir(i):
        convert_video_dir(i, video_format, others)
    else:
        color.print_err('param i is neigher video file nor directory')








def interactive():

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



if __name__ == '__main__':

    test_ffmpeg()
    interactive()