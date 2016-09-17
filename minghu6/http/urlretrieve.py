# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
About :urlretrieve ... download
################################################################################
"""

def report(count, block_size, total_size):
    """

    :param count:
    :param block_size:
    :param total_size:
    :return:
    """
    import sys

    download_size=count*block_size
    percent = int(download_size*100/total_size)
    sys.stdout.write(('\rdownload ...{0:d}%'
                      '\t\t{1:f} Mb').format(percent,download_size/10e5))
    sys.stdout.flush()

from minghu6.etc.version import iswin,islinux

from minghu6.text.color import color
import sys

plus = '█'
def get_progress_bar(now_size, total_size, max_length=25,extra_str=''):
    """

    :param now_size:
    :param total_size:
    :param max_length:
    :return:
    """
    now_length = int(now_size * max_length / total_size)

    progress = plus*now_length+(max_length - now_length)*2*' '+extra_str

    progress_bar = progress

    return progress_bar


def report_color(count, block_size, total_size):

    download_size=count * block_size
    percent = (download_size * 100 / total_size)

    pts=('\rdownload ...'
         '\t{0:.3f} mb ').format(download_size / 10e5)
    pts2=get_progress_bar(download_size, total_size,
                          extra_str='{0:.2f}%'.format(percent))

    pts=''.join([pts, pts2])
    sys.stdout.flush()
    color.print_info(pts,end='',flush=True)



if __name__ == '__main__':

    for i in range(10):
        report_color(5,10,100)
