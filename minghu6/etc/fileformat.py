# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
A Simple Formatter，
(more complex and more efficient libarary, recommend python-magic)
"""
import struct
import os
import json

from minghu6.algs.var import each_same
from minghu6.io.stream import hexStr_bytesIter
from minghu6.etc.cmd import exec_cmd, has_proper_ffprobe

from collections import namedtuple

__all__ = ['FileTypePair',
           'UNKNOWN_TYPE',
           'fileformat',
           'DoNotSupportThisExt',
           'convert_img']


FileTypePair = namedtuple('FileTypePair',
                        ['normal_name', 'ext_name'])


# MS Word/Excel (xls.or.doc)	D0CF11E0
# Postscript (eps.or.ps)	252150532D41646F6265
# MPEG (mpg)	000001BA
# MPEG (mpg)	000001B3
UNKNOWN_TYPE = "unknown"
highBytes_typeDict={"FFD8FF"    : FileTypePair("JPEG", "jpg"),
                    "89504E47"  : FileTypePair("PNG", "png"),
                    "47494638"  : FileTypePair("GIF", "gif"),
                    "49492A00"  : FileTypePair("TIFF", "tif"),
                    "424D"      : FileTypePair("Windows Bitmap", "bmp"),
                    "41433130"  : FileTypePair("CAD", "dwg"),
                    "38425053"  : FileTypePair("Adobe Photoshop", "psd"),
                    "7B5C727466": FileTypePair("Rich Text Format", "rtf"),
                    "3C3F786D6C": FileTypePair("XML", "xml"),
                    "68746D6C3E": FileTypePair("HTML", "html"),
                    "44656C69766572792D646174653A" : FileTypePair("Email", "eml"),
                    "CFAD12FEC5FD746F" : FileTypePair("Outlook Express", "dbx"),
                    "2142444E"  : FileTypePair("Outlook", "pst"),
                    "5374616E64617264204A" : FileTypePair("MS Access", "mdb"),
                    "FF575043"  : FileTypePair("WordPerfect", "wpd"),
                    "252150532D41646F6265" : FileTypePair("Postscript", "ps"),
                    "255044462D312E" : FileTypePair("Adobe Acrobat", "pdf"),
                    "AC9EBD8F"  : FileTypePair("Quicken", "qdf"),
                    "E3828596"  : FileTypePair("Windows Password", "pwl"),
                    "504B0304"  : FileTypePair("ZIP Archive", "zip"),
                    "52617221"  : FileTypePair("RAR Archive", "rar"),
                    "57415645"  : FileTypePair("Wave", "wav"),
                    "41564920"  : FileTypePair("AVI", "avi"),
                    "2E7261FD"  : FileTypePair("Real Audio", "ram"),
                    "2E524D46"  : FileTypePair("Real Media", "rm"),
                    "000001BA"  : FileTypePair("MPEG", "mpg"),
                    "000001B3"  : FileTypePair("MPEG", "mpg"),
                    "6D6F6F76"  : FileTypePair("Quicktime", "mov"),
                    "3026B2758E66CF11" : FileTypePair("Windows Media", "asf"),
                    "4D546864"  : FileTypePair("MIDI", "mid")


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

            if each_same(hexStr_bytesIter(hcode), hbytes):
                fformat = tl[hcode]
                break

    if fformat == UNKNOWN_TYPE:
        # continue to recognise
        if has_proper_ffprobe():
            cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams %s' % path
            info_lines, _ = exec_cmd(cmd)
            s = '\n'.join(info_lines)
            json_obj = json.loads(s)
            try:
                normal_name = json_obj['streams'][0]['codec_name']
                ext_name = json_obj['format']['format_name']
            except KeyError:
                pass
            else:
                fformat = FileTypePair(normal_name, ext_name)

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




