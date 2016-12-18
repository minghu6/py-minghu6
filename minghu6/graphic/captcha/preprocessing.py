# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

import PIL
from PIL import Image, ImageDraw, ImageEnhance
import os


#此函数用于设置像素值的转换，
def set_table(a):
    table=[]
    for i in range(256):
        if i<a:
            table.append(0)
        else:
            table.append(1)
    return table


def binary_img(imgObj, a=100):
    imgObj = imgObj.copy()

    img1=imgObj.convert("L")
    img2=img1.point(set_table(a), '1')

    return img2

def sharpen_img(imgObj):
    imgObj = imgObj.copy()

    imgObj = ImageEnhance.Sharpness(imgObj.convert('RGB')).enhance(3)
    return imgObj


# 降噪
def clearNoise_img(imgObj):
    imgObj = imgObj.copy()
    if imgObj.mode not in  {'1', 'P'}:
        imgObj = imgObj.convert('P')

    w,h = imgObj.size
    pixdata = imgObj.load()

    for y in range(1, h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255

    return imgObj


def removeFrame_img(imgObj, frame_width=2):
    imgObj = imgObj.copy()

    (width, height) = imgObj.size
    imgObj = imgObj.crop((frame_width, frame_width,
                          width - frame_width, height-frame_width))

    return imgObj

def boxsplit_img(imgObj, n=None):
    """
    split imgobj to many single-character imgs
    Warning: size are not fixed!
    :param imgobj:
    :return:
    """


    img2=binary_img(imgObj)
    #img2 = img1
    pix2=img2.load()
    (width, height)=img2.size

    x0=[]
    y0=[]

    #x表示行，y表示列
    #x0中存储列的位置，y0存储列每个列中像素为0（黑点）的个数
    for x in range(0, width):
        col_spot_num=0
        for y in range(1, height):
            if pix2[x,y]==0:
                col_spot_num += 1

        y0.append(col_spot_num)
        if col_spot_num>0:
            x0.append(x)

    count=[]
    for i in range(0, len(x0)-1):
        if (i-1)!=-1:
            if x0[i]-x0[i-1]>1 and x0[i+1]-x0[i]>1:
                count.append(i)

    for i in range(len(count)-1, -1, -1):  #逆向删除，是考虑到移除数据时，后面的数据会向前移动
        x0.remove(x0[count[i]])

    if x0[1]-x0[0]>1:   #之前的循环没有检查x0[0]
        x0.remove(x0[0])
    if x0[-1]-x0[-2]>1:  #和x0[-1]
        x0.remove(x0[-1])


    z=[]
    z.append(x0[0])
    for j in range(0, len(x0)-1):

        if(x0[j+1]-x0[j])>1:

            z.append(x0[j])
            z.append(x0[j+1])


    z.append(x0[-1])

    import itertools
    start = itertools.islice(z, 0, None, 2)
    end = itertools.islice(z, 1, None, 2)

    box = []

    for s, e in zip(start, end):
        box.append((s, 0, e, height))


    result= []
    for square in box:
        result.append(imgObj.crop(square)) # don't binazation

    return result


def bisect_img(imgobj, n):
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
        x = i*incx   # 里的数字参数需要自己
        y = height   # 证码图片的像素进行
        imgs.append(imgobj.crop((x, 0, x+incx, y)))

    return imgs


if __name__ == '__main__':
    pass