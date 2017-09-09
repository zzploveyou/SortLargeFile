# coding:utf-8

import os
import random

def getRandomGFile(filename, G):
    """
    生成一个G 级的随机数大文件.
    """
    size = G*1024*1024*1024
    with open(filename, 'w') as f:
        while os.path.getsize(filename) < size:
            for i in range(10000000):
                f.write("{}\n".format(random.random()))

def getRandomFile(filename, num):
    with open(filename, 'w') as f:
        for i in range(int(num)):
            f.write("{}\n".format(random.random()))

if __name__ == '__main__':
    import sys
    try:
        par = sys.argv[1]
        if par.isdigit():
            getRandomFile("BigFile.txt", int(par))
        else:
            getRandomGFile("BigFile.txt", G=float(sys.argv[1]))
    except Exception as e:
        print("error:{}".format(e))
        print("""You need one float parameter as the G size of file or one int parameter as the line number of file.""")
