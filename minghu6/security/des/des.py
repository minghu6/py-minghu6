# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Des Implement
################################################################################
"""

#IP置换表
IP_table=[58, 50, 42, 34, 26, 18, 10,  2,
          60, 52, 44, 36, 28, 20, 12,  4,
          62, 54, 46, 38, 30, 22, 14,  6,
          64, 56, 48, 40, 32, 24, 16,  8,
          57, 49, 41, 33, 25, 17,  9,  1,
          59, 51, 43, 35, 27, 19, 11,  3,
          61, 53, 45, 37, 29, 21, 13,  5,
          63, 55, 47, 39, 31, 23, 15,  7
          ]
#逆IP置换表
_IP_table=[40,  8, 48, 16, 56, 24, 64, 32,
           39,  7, 47, 15, 55, 23, 63, 31,
           38,  6, 46, 14, 54, 22, 62, 30,
           37,  5, 45, 13, 53, 21, 61, 29,
           36,  4, 44, 12, 52, 20, 60, 28,
           35,  3, 43, 11, 51, 19, 59, 27,
           34,  2, 42, 10, 50, 18, 58, 26,
           33,  1, 41,  9, 49, 17, 57, 25
           ]
#S盒中的S1盒
S1=[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
    0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
    4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
    15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ]
#S盒中的S2盒
S2=[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
    3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
    0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
    13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
    ]
#S盒中的S3盒
S3=[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
    13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
    13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
    1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
    ]
#S盒中的S4盒
S4=[7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
    13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
    10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
    3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ]
#S盒中的S5盒
S5=[2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
    14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
    4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
    11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ]
#S盒中的S6盒
S6=[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
    10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
    9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
    4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ]
#S盒中的S7盒
S7=[4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
    13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
    1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
    6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ]
#S盒中的S8盒
S8=[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
    1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
    7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
    2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    ]
# S盒
S=[S1,S2,S3,S4,S5,S6,S7,S8]
#P盒
P_table=[16,  7, 20, 21,
         29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
         32, 27,  3,  9,
         19, 13, 30,  6,
         22, 11,  4, 25
         ]

#压缩置换表1，不考虑每字节的第8位，将64位密钥减至56位。然后进行一次密钥置换。
compress_table1=[ 57, 49, 41, 33, 25, 17,  9,
                  1, 58, 50, 42, 34, 26, 18,
                  10,  2, 59, 51, 43, 35, 27,
                  19, 11,  3, 60, 52, 44, 36,
                  63, 55, 47, 39, 31, 23, 15,
                  7, 62, 54, 46, 38, 30, 22,
                  14,  6, 61, 53, 45, 37, 29,
                  21, 13,  5, 28, 20, 12,  4
                  ]

#压缩置换表2，用于将循环左移和右移后的56bit密钥压缩为48bit
compress_table2=[14, 17, 11, 24,  1,  5,
                 3, 28, 15,  6, 21, 10,
                 23, 19, 12,  4, 26,  8,
                 16,  7, 27, 20, 13,  2,
                 41, 52, 31, 37, 47, 55,
                 30, 40, 51, 45, 33, 48,
                 44, 49, 39, 56, 34, 53,
                 46, 42, 50, 36, 29, 32
                 ]


#用于对数据进行扩展置换，将32bit数据扩展为48bit
extend_table=[32,  1,  2,  3,  4,  5,
              4,  5,  6,  7,  8,  9,
              8,  9, 10, 11, 12, 13,
              12, 13, 14, 15, 16, 17,
              16, 17, 18, 19, 20, 21,
              20, 21, 22, 23, 24, 25,
              24, 25, 26, 27, 28, 29,
              28, 29, 30, 31, 32,1]



def char2unicode_ascii(intext):
    outtext=[ord(intext[i]) for i in range(len(intext))]
    return outtext

#将8位ASCII码转为bit
def byte2bit(inchar):

    #一次左移一bit
    outbit = [inchar[int(i/8)]>>(i%8)&1 for i in range(len(inchar)*8)]
    return outbit

#将Unicode码转为bit
def unicode2bit(intext):

    #一次左移一bit
    outbit = [intext[int(i/16)]>>(i%16)&1 for i in range(len(intext)*16)]
    return outbit

#将bit转为Unicode码
def bit2unicode(inbit):
    out=[]
    temp=0
    for i in range(len(inbit)):
        temp=temp|(inbit[i]<<(i%16))
        if i%16==15:
            out.append(temp)
            temp=0
    return out

#将unicode码转为字符（中文或英文）
def unicode2char(inbyte):
    out = ''.join([chr(inbyte[i]) for i in range(len(inbyte))])
    return out

#将bit转为ascii 码
def bit2byte(inbit):
    out=[]
    temp=0
    for i in range(len(inbit)):
        temp=temp|(inbit[i]<<(i%8))
        if i%8==7:
            out.append(temp)
            temp=0
    return out



#生成每一轮的key
def createKeys(inkeys):
    keyResult=[]
    keyinit=byte2bit(char2unicode_ascii(inkeys))
#    print("keyinit=",end='')
#    print(keyinit)
    #初始化列表key0,key1
    key0=[0 for i in range(56)]
    key1=[0 for i in range(48)]
    #进行密码压缩置换1，将64位密码压缩为56位
    #print('key[0]:{0}, keyinit: {1}, compress_table1: {2} '.format(len(key0), len(keyinit), len(compress_table1)))
    for i in range(56):
        key0[i]=keyinit[compress_table1[i]-1]

    #进行16轮的密码生成
    for i in range(16):
        #---------确定左移的次数----------
        if (i==0 or i==1 or i==8 or i==15):
            moveStep=1
        else:
            moveStep=2
        #------------------------------

        #--------分两部分，每28bit位一部分，进行循环左移------------
        for j in range(moveStep):
            for k in range(8):
                temp=key0[k*7]
                for m in range(7*k,7*k+6):
                    key0[m]=key0[m+1]
                key0[k*7+6]=temp
            temp=key0[0]
            for k in range(27):
                key0[k]=key0[k+1]
            key0[27]=temp
            temp=key0[28]
            for k in  range(28,55):
                key0[k]=key0[k+1]
            key0[55]=temp
        #-----------------------------------------------------


        #------------对56位密钥进行压缩置换，压缩为48位-------------
        for k in range(48):
            key1[k]=key0[compress_table2[k]-1]
        keyResult.extend(key1)



        #------------------------------------------------------

    return keyResult


def DES(text, key, optionType):
    keyResult=createKeys(key)
    finalTextOfBit=[0 for i in range(64)]
    finalTextOfUnicode=[0 for i in range(4)]
    #print(keyResult)

    if optionType==0:#选择的操作类型为加密

        tempText=[0 for i in range(64)]#用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR=[0 for i in range(48)] #用于盛放R部分的扩展结果
        unicodeText=char2unicode_ascii(text)
        #print(unicodeText)
        bitText=unicode2bit(unicodeText)
        #print(bitText)

        initTrans=[0 for i in range(64)]#初始化，用于存放IP置换后的结果

        #------------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i]=bitText[IP_table[i]-1]
        #将64位明文分为左右两部分
        L=[initTrans[i] for i in range(32)]
        R=[initTrans[i] for i in range(32,64)]


        #开始进行16轮运算
        for i in range(16):
            tempR=R #用于临时盛放R

            #-----------进行扩展，将32位扩展为48位--------
            for j in range(48):
                extendR[j]=R[extend_table[j]-1]
            #print(len(keyResult))
            keyi=[keyResult[j] for j in range(i*48,i*48+48)]
            #----------与key值进行异或运算----------------
            XORResult=[0 for j in range(48)]
            for j in range(48):
                if keyi[j]!=extendR[j]:
                    XORResult[j]=1

            SResult=[0 for k in range(32)]
             #---------开始进行S盒替换-------------------
            for k in range(8):
                row=XORResult[k*6]*2+XORResult[k*6+5]
                column=XORResult[k*6+1]*8+XORResult[k*6+2]*4+XORResult[k*6+3]*2+XORResult[k*6+4]
                temp=S[k][row*16+column]
                for m in range(4):
                    SResult[k*4+m]=(temp>>m)&1
            #-----------------------------------------
            PResult=[0 for k in range(32)]
            #--------------开始进行P盒置换----------------
            for k in range(32):
                PResult[k]=SResult[P_table[k]-1]
            #------------------------------------------


            #--------------与L部分的数据进行异或------------
            XORWithL=[0 for k in range(32)]
            for k in range(32):
                if L[k]!=PResult[k]:
                    XORWithL[k]=1
            #----------------------------------------------


            #-------------将临时保存的R部分值，即tempR复制给L------
            L=tempR
            R=XORWithL

        #----交换左右两部分------
        L,R=R,L

        #-----合并为一部分
        tempText=L
        tempText.extend(R)
        #-----------IP逆置换--------
        for k in range(64):
            finalTextOfBit[k]=tempText[_IP_table[k]-1]
        finalTextOfUnicode=bit2byte(finalTextOfBit)
        #print(finalTextOfUnicode)
        finalTextOfChar=unicode2char(finalTextOfUnicode)
        #print(finalTextOfChar)
        return finalTextOfChar
    else:#选择的操作类型为解密


        tempText=[0 for i in range(64)]#用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR=[0 for i in range(48)]#用于盛放R部分的扩展结果
        unicodeText=char2unicode_ascii(text)
        #print(unicodeText)
        bitText=byte2bit(unicodeText)
        #print(bitText)

        initTrans=[0 for i in range(64)]#初始化，用于存放IP置换后的结果

        #------------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i]=bitText[IP_table[i]-1]
        #将64位明文分为左右两部分
        L=[initTrans[i] for i in range(32)]
        R=[initTrans[i] for i in range(32,64)]



        #-----------------开始16轮的循环-----------------
        for i in range(15,-1,-1):
            tempR=R #用于临时盛放R

            #-----------进行扩展，将32位扩展为48位--------
            for j in range(48):
                extendR[j]=R[extend_table[j]-1]

            keyi=[keyResult[j] for j in range(i*48,i*48+48)]
            #----------与key值进行异或运算----------------
            XORResult=[0 for j in range(48)]
            for j in range(48):
                if keyi[j]!=extendR[j]:
                    XORResult[j]=1

            SResult=[0 for k in range(32)]
             #---------开始进行S盒替换-------------------
            for k in range(8):
                row=XORResult[k*6]*2+XORResult[k*6+5]
                column=XORResult[k*6+1]*8+XORResult[k*6+2]*4+XORResult[k*6+3]*2+XORResult[k*6+4]
                temp=S[k][row*16+column]
                for m in range(4):
                    SResult[k*4+m]=(temp>>m)&1
            #-----------------------------------------
            PResult=[0 for k in range(32)]
            #--------------开始进行P盒置换----------------
            for k in range(32):
                PResult[k]=SResult[P_table[k]-1]
            #------------------------------------------


            #--------------与L部分的数据进行异或------------
            XORWithL=[0 for k in range(32)]
            for k in range(32):
                if L[k]!=PResult[k]:
                    XORWithL[k]=1
            #----------------------------------------------


            #-------------将临时保存的R部分值，即tempR复制给L------
            L=tempR
            R=XORWithL

        #----交换左右两部分------
        L,R=R,L

        #-----合并为一部分
        tempText=L
        tempText.extend(R)
        #-----------IP逆置换--------
        for k in range(64):
            finalTextOfBit[k]=tempText[_IP_table[k]-1]
        finalTextOfUnicode=bit2unicode(finalTextOfBit)
        #print(finalTextOfUnicode)
        finalTextOfChar=unicode2char(finalTextOfUnicode)
        #print(finalTextOfChar)
        return finalTextOfChar



def encryp_str(M, key):
    """
    DES encrption
    format to 4 *, /u0020 space
    :param M:   str
    :param key: 64 bit -- len(key)==8
    :return:    C -- str
    """
    assert isinstance(M, str)
    assert isinstance(key, str) and len(key) == 8

    def char2unicode_ascii_hex(intext):
        outtext=''.join([hex(ord(intext[i])) for i in range(len(intext))])
        return outtext


    if len(M) % 4 !=0:
        M = M + '\u0020'*(4-len(M)%4)

    C = []

    for i in range(len(M))[slice(0,len(M),4)]:
        #print(i)
        C.append(char2unicode_ascii_hex(DES(M[i:i+4], key, 0)))

    C = ''.join(C)


    return C


def decryp_str(C, key):
    """
    DES decrption
    Must is  8 *
    :param C:   str
    :param key: 64 bit -- len(key)==8
    :return:    M -- str
    """
    assert isinstance(C, str)
    assert isinstance(key, str) and len(key) == 8

    C = C.lower().split('0x')[1:]

    assert len(C) % 8 ==0

    #print('len(C)', len(C))
    def hexstr2chr(hexstr):
        '''
        :param hexstr_list:
        :return: list of str
        '''

        chrstr = ''.join([chr(int(i,base=16)) for i in hexstr])
        return  chrstr

    C = hexstr2chr(C)
    M = []
    for i in range(len(C))[slice(0,len(C),8)]:
        #print(i,C[i:i+8],end='')
        M.append(DES(C[i:i+8], key, 1))

    M = ''.join(M)

    return M


def __test_basic():
    passwd = '12345678'

    M='''DES( Data DES( Data Encryption Standard)算法，\n
            于1977年得到美国政府的正式许可，\n
            是一种用56位密钥来加密64位数据的方法。\n'''

    #M = '同志们好'
    print('origin M: ',M)
    print('len(origin M)', len(M))
    C = encryp_str(M, passwd)

    M = decryp_str(C, passwd)
    print('\nM', M)
    print('len(M)', len(M))

if __name__ == '__main__':

    __test_basic()
    pass