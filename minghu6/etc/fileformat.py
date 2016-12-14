# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
A Simple Formatter，
(more complex and more efficient libarary, recommend python-magic)
"""
import struct
import os

from minghu6.algs.var import allequal
from minghu6.io.stream import hexStr_bytesIter

from collections import namedtuple

filetype_name_pair = namedtuple('filetype_name_pair',
                                ['normal_name', 'ext_name'])


# MS Word/Excel (xls.or.doc)	D0CF11E0
# Postscript (eps.or.ps)	252150532D41646F6265
# MPEG (mpg)	000001BA
# MPEG (mpg)	000001B3
UNKNOWN_TYPE = "unknown"
highBytes_typeDict={"FFD8FF"    : filetype_name_pair("JPEG", "jpg"),
                    "89504E47"  : filetype_name_pair("PNG", "png"),
                    "47494638"  : filetype_name_pair("GIF", "gif"),
                    "49492A00"  : filetype_name_pair("TIFF", "tif"),
                    "424D"      : filetype_name_pair("Windows Bitmap", "bmp"),
                    "41433130"  : filetype_name_pair("CAD", "dwg"),
                    "38425053"  : filetype_name_pair("Adobe Photoshop", "psd"),
                    "7B5C727466": filetype_name_pair("Rich Text Format", "rtf"),
                    "3C3F786D6C": filetype_name_pair("XML", "xml"),
                    "68746D6C3E": filetype_name_pair("HTML", "html"),
                    "44656C69766572792D646174653A" : filetype_name_pair("Email", "eml"),
                    "CFAD12FEC5FD746F" : filetype_name_pair("Outlook Express", "dbx"),
                    "2142444E"  : filetype_name_pair("Outlook", "pst"),
                    "5374616E64617264204A" : filetype_name_pair("MS Access", "mdb"),
                    "FF575043"  : filetype_name_pair("WordPerfect", "wpd"),
                    "252150532D41646F6265" : filetype_name_pair("Postscript", "ps"),
                    "255044462D312E" : filetype_name_pair("Adobe Acrobat", "pdf"),
                    "AC9EBD8F"  : filetype_name_pair("Quicken", "qdf"),
                    "E3828596"  : filetype_name_pair("Windows Password", "pwl"),
                    "504B0304"  : filetype_name_pair("ZIP Archive", "zip"),
                    "52617221"  : filetype_name_pair("RAR Archive", "rar"),
                    "57415645"  : filetype_name_pair("Wave", "wav"),
                    "41564920"  : filetype_name_pair("AVI", "avi"),
                    "2E7261FD"  : filetype_name_pair("Real Audio", "ram"),
                    "2E524D46"  : filetype_name_pair("Real Media", "rm"),
                    "000001BA"  : filetype_name_pair("MPEG", "mpg"),
                    "000001B3"  : filetype_name_pair("MPEG", "mpg"),
                    "6D6F6F76"  : filetype_name_pair("Quicktime", "mov"),
                    "3026B2758E66CF11" : filetype_name_pair("Windows Media", "asf"),
                    "4D546864"  : filetype_name_pair("MIDI", "mid")


                   }

# 获取文件类型
def fileformat(path):
    with open(path, 'rb') as binfile:# 必需二制字读取
        tl = highBytes_typeDict
        fformat = UNKNOWN_TYPE
        for hcode in tl.keys():
            numOfBytes = len(hcode) // 2 # 需要读多少字节
            binfile.seek(0)              # 每次读取都要回到文件头，不然会一直往后读取
            hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节

            if allequal(hexStr_bytesIter(hcode), hbytes):
                fformat = tl[hcode]
                break
    return fformat

class DoNotSupportThisExt(BaseException):pass

def convert_img(path, ext, outdir=os.curdir):
    """

    :param path:
    :param img_format: such as png, gif etc.
    :param outdir:
    :return:
    """
    from PIL  import Image
    imgObj = Image.open(path)
    oldImg_format = imgObj.format
    imgObj = imgObj.convert('RGB')

    fn = os.path.basename(path)
    output = os.path.join(outdir, os.path.splitext(fn)[0]+'.'+ext)

    img_extFormat_dict = {
        'jpg' : 'JPEG',
        'bmp' : 'BMP',
        'tif' : 'TIFF',
        'gif' : 'GIF',
        'PNG' : 'png',
    }
    try:
        newImg_format = img_extFormat_dict[ext]
    except KeyError:
        raise DoNotSupportThisExt

    if oldImg_format.lower() != ext.lower():
        imgObj.save(output, newImg_format)




