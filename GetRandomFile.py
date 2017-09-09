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

if __name__ == '__main__':
    import sys
    try:
        getRandomGFile("BigFile.txt", G=float(sys.argv[1]))
    except:
        print("""Usage: python GetRandomFile.py 1,
            You need one float parameter as the size of file.""")
