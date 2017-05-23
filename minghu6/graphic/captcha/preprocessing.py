# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
#TODO Developing...
"""
from collections import Counter
from functools import partial

import numpy as np
from PIL import ImageEnhance
from PIL.Image import Image

__all__ = ['binary_img',
           'sharpen_img',
           'clearNoise_img',
           'removeFrame_img',
           'bisect_img']


# PIL
def set_table(a):
    table = []
    for i in range(256):
        if i < a:
            table.append(0)
        else:
            table.append(1)
    return table


def binary_img(imgObj: Image, a=100):
    imgObj = imgObj.copy()

    img1 = imgObj.convert("L")
    img2 = img1.point(set_table(a), '1')

    return img2


def sharpen_img(imgObj: Image):
    imgObj = imgObj.copy()

    imgObj = ImageEnhance.Sharpness(imgObj.convert('RGB')).enhance(3)
    return imgObj


def clearNoise_img(imgObj: Image):
    imgObj = imgObj.copy()
    if imgObj.mode not in {'1', 'P'}:
        imgObj = imgObj.convert('P')

    w, h = imgObj.size
    pixdata = imgObj.load()

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:
                count = count + 1
            if pixdata[x, y + 1] > 245:
                count = count + 1
            if pixdata[x - 1, y] > 245:
                count = count + 1
            if pixdata[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x, y] = 255

    return imgObj


class ImageSizeError(BaseException): pass


def removeFrame_img(imgObj: Image, frame_width=2):
    imgObj = imgObj.copy()

    (width, height) = imgObj.size
    if frame_width >= width or frame_width >= height:
        raise ImageSizeError('image size too small, (%s, %s)' % imgObj.size)

    imgObj = imgObj.crop((frame_width, frame_width,
                          width - frame_width, height - frame_width))

    return imgObj


def bisect_img(imgobj: Image, n):
    """
    split imgobj to single-character img
    using avarage width
    :param imgobj:
    :param n:
    :return:
    """
    (width, height) = imgobj.size
    img_slice = width // n
    imgs = []
    incx = img_slice
    for i in range(n):
        x = i * incx  # 里的数字参数需要自己
        y = height  # 证码图片的像素进行
        imgs.append(imgobj.crop((x, 0, x + incx, y)))

    return imgs


# OpenCV + numpy
def _isvalid_point(x, y, h, w):
    if x >= 0 and x < h and y >= 0 and y < w:
        return True
    else:
        return False


def clear_single_noise(im: np.ndarray, threshold=140):  # threshold for blank point!!
    """im is instance of numpy.array, gray image,
    clear single point noise
    """
    h, w = im.shape

    isvalid = partial(_isvalid_point, w=w, h=h)
    noise_point_set = []
    for x in range(h):
        for y in range(w):
            blank_count = 0
            valid_count = 0
            if isvalid(x - 1, y): valid_count += 1
            if isvalid(x + 1, y): valid_count += 1
            if isvalid(x, y - 1): valid_count += 1
            if isvalid(x, y + 1): valid_count += 1

            if isvalid(x - 1, y - 1): valid_count += 1
            if isvalid(x + 1, y - 1): valid_count += 1
            if isvalid(x - 1, y + 1): valid_count += 1
            if isvalid(x + 1, y + 1): valid_count += 1

            if isvalid(x - 1, y) and im[x - 1, y] >= threshold:  # up
                blank_count += 1

            if isvalid(x + 1, y) and im[x + 1, y] >= threshold:  # down
                blank_count += 1

            if isvalid(x, y - 1) and im[x, y - 1] >= threshold:  # left
                blank_count += 1

            if isvalid(x, y + 1) and im[x, y + 1] >= threshold:  # right
                blank_count += 1

            if isvalid(x - 1, y - 1) and im[x - 1, y - 1] >= threshold:  # uppper left
                blank_count += 1

            if isvalid(x + 1, y - 1) and im[x + 1, y - 1] >= threshold:  # bottom left
                blank_count += 1

            if isvalid(x - 1, y + 1) and im[x - 1, y + 1] >= threshold:  # upper right
                blank_count += 1

            if isvalid(x + 1, y + 1) and im[x + 1, y + 1] >= threshold:  # bottom right
                blank_count += 1

            if blank_count == valid_count:
                # print(x,y, blank_count)
                noise_point_set.append((x, y))

    for x, y in noise_point_set:
        im[x, y] = threshold

    return im


def format_letter(im: np.ndarray, out_height=32, out_width=32):
    """format size of image"""

    offset_x = int(abs(out_height - im.shape[0]) / 2)
    offset_y = int(abs(out_width - im.shape[1]) / 2)

    im_height, im_width = im.shape

    out = np.ones((out_height, out_width)) * 255
    out[offset_x: offset_x + im_height, offset_y: offset_y + im_width] = im

    return out


def horizontal_project(im: np.ndarray, threshold=0):
    projection = []
    width = im.shape[1]
    for j in range(width):
        projection.append(Counter(im[:, j])[threshold])  # black pot number

    return projection


def vertical_project(im: np.ndarray, threshold=0):
    projection = []
    height = im.shape[0]
    for i in range(height):
        projection.append(Counter(im[i, :])[threshold])  # black pot number

    return projection


def compute_cutline(projection, only_one=False):
    "x0, x1 all included"
    state = 'start'
    break_pos = []
    x0 = None
    x1 = None
    zero_count = 0

    for i, n in enumerate(projection):

        if state == 'start':
            if n == 0:
                state = 'zero'
            else:
                state = 'none-zero'
                x0 = i

        elif state == 'zero':
            if n != 0:
                state = 'none-zero'
                x0 = i

        elif state == 'none-zero':
            if n == 0:
                state = 'zero'
                x1 = i
                break_pos.append((x0, x1))

    if only_one and len(break_pos) > 1:
        break_pos = [(break_pos[0][0], break_pos[-1][1])]

    return break_pos


def _split_letters_projection(im_b: np.ndarray):
    projection_h = horizontal_project(im_b)
    cutlines_h = compute_cutline(projection_h)
    image_split_v = [im_b[:, line[0]:line[1]] for line in cutlines_h]

    letters = []
    for i, each_image_split_v in enumerate(image_split_v):
        projection_v = vertical_project(each_image_split_v)
        cutlines_v = compute_cutline(projection_v, only_one=True)
        # print(cutlines_v)
        line = cutlines_v[0]
        letters.append(image_split_v[i][line[0]:line[1], :])

    return letters


def boxsplit_img(imgobj: Image, n=None):
    pass


if __name__ == '__main__':
    pass
