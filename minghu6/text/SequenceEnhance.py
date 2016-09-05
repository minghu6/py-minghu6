
# coding: utf-8

# In[15]:
import sys

def split_whitespace(src):
    src=src.strip()
    import re
    return re.split('\s+',src)


def parseInts(Iteration):
    ints=[int(cell) for cell in Iteration]
    return ints

def parseStr(Iteration):
    ss=[item.strip() for item in Iteration]
    return ss


invalid_char_set={'\\','/',':','*','?','"','<','>','|'}
def filter_invalid_char(basefn,invalid_set=invalid_char_set):

    return ''.join((list(filter(lambda x:x not in invalid_set,basefn))))

def self_input(prompt=''):
    '''Implement with BIF input()'''
    src=split_whitespace(input(prompt))
    while len(src[0])==0:
        #print('??')
        src=split_whitespace(input())
    
    return src


def self_input_eh(stream_in=sys.stdin,stream_out=sys.stdout,prompt=''):

    stream_out.write(prompt)
    src=split_whitespace(stream_in.readline())
    while len(src[0])==0:
        #print('??')
        src=split_whitespace(stream_in.readline())
    
    return src

if __name__=='__main__':

    #src=self_input_eh(prompt='输入两个数\n')
    src=self_input_eh(open(
        'E:\Coding\Java\myscripts\MyselfPackage\Minghu6JavaClass\dist\README.TXT'))
    print(src)
