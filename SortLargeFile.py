# coding:utf-8

import argparse
import os
import sys
from collections import defaultdict
from time import ctime


class RSNode:
    """node of Replace_Selection method"""

    def __init__(self, rowNum, value, freader_ind=None):
        """
        constructor of RSNode

        Parameters
        ----------
        rowNum: int
            index of merge part.
        value: string
            value of RSNode.
        freader_ind: int
            default: None
            index of filereader.
        """
        self.rowNum = rowNum
        self.value = value
        self.freader_ind = freader_ind


class LoserTree:
    """loserTree"""

    def __init__(self, n):
        """
        constructor of LoserTree.

        Parameters
        ----------
        n: int
            size of LoserTree.
        """

        self.loserTree = [0] * n
        self.dataArray = [RSNode(1, i - n) for i in range(n)]
        self.n = n
        for i in range(n):
            self.adjust(n - 1 - i)

    def adjust(self, s):
        """
        adjust the position of dataArray[s] in loserTree.

        Parameters
        ----------
        s: int
            index of data.
        """
        t = (s + self.n) / 2
        while t > 0:
            # rowNum has a higher Priority than value.
            if self.dataArray[s].rowNum > self.dataArray[self.loserTree[t]].rowNum:
                s, self.loserTree[t] = self.loserTree[t], s
            elif self.dataArray[s].rowNum == self.dataArray[self.loserTree[t]].rowNum \
                    and self.dataArray[s].value > self.dataArray[self.loserTree[t]].value:
                # switch position of s and its father.
                s, self.loserTree[t] = self.loserTree[t], s
            t /= 2
        self.loserTree[0] = s


class SortLargeFile:
    """Sort Large File"""

    def __init__(self, LargeFile, tarDir, n):
        """
        constructor of SortLargeFile.

        Parameters
        ----------
        LargeFile: str
            path of large file.
        tarDir: str
            path of target directory.
        n: int
            number of RSNodes that in memory.
        """
        self.LargeFile = LargeFile
        self.fr = open(self.LargeFile, 'r')
        self.tarDir = tarDir
        self.n = int(n)
        self.sizes = defaultdict(lambda: 0)
        self.sonfileNum = 1  # 归并段序号,也即子文件标识
        self.tmp = []  # 内存中现在存放的数据
        self.MINIMAX = 0
        self.CONSTANT = [""]  # 一个固定的值, 非string类型即可
        self.NUM_FILE = 0  # 记录文件的总行数

    def nfilename(self, n):
        """
        generate sonfile name.
        Parameters
        ----------
        n: int
            index of file.
        """
        return os.path.join(self.tarDir, '{}-son-{}.txt'.format(
            os.path.basename(os.path.splitext(self.LargeFile)[0]), n))

    def writetmp(self, filename):
        """
        write tmp data to filename.
        """
        if self.tmp == [''] or self.sonfileNum > 10000:
            print("Empty son file, maybe somthing is wrong.")
            self.fr.close()
            sys.exit(1)
        with open(filename, 'a+') as fw:
            self.sizes[filename] += len(self.tmp)  # 记录文件大小
            fw.writelines(self.tmp)
        while self.tmp:
            self.tmp.pop()

    def rsnode(self, line=None):
        """
        return RSNode.
        Parameters
        ----------
        line: str
            default: None
            data of the RSNode.
        """
        if line:
            return RSNode(self.sonfileNum, line)
        else:
            # 标号+100, 以示区分
            return RSNode(self.sonfileNum + 100, self.CONSTANT)

    def readline(self):
        """
        read line of LargeFile, and count number.
        """
        line = self.fr.readline()
        if line != "":
            self.NUM_FILE += 1
        return line

    def replace_selection(self, ltree, line, final=False):
        """
        replace and selection algorithm.
        Parameters
        ----------
        ltree: loserTree
            loserTree.
        line: str
            data in LargeFile.
        final: bool
            if final==True:
                get data left in losertree.
        """
        if final:
            ltree.dataArray[ltree.loserTree[0]] = self.rsnode()
        else:
            ltree.dataArray[ltree.loserTree[0]] = self.rsnode(line)
        while True:
            if len(self.tmp) == self.n:
                self.writetmp(self.nfilename(self.sonfileNum))
            ltree.adjust(ltree.loserTree[0])

            if final and ltree.dataArray[ltree.loserTree[0]].value == self.CONSTANT:
                break

            if ltree.dataArray[ltree.loserTree[0]].rowNum > self.sonfileNum:
                self.writetmp(self.nfilename(self.sonfileNum))
                self.sonfileNum += 1
                self.MINIMAX = ltree.dataArray[ltree.loserTree[0]]
                self.tmp.append(self.MINIMAX.value)
                if final:
                    ltree.dataArray[ltree.loserTree[0]] = self.rsnode()
                else:
                    line = self.readline()
                    if line:  # Reach the end of the file
                        ltree.dataArray[ltree.loserTree[0]] = self.rsnode(line)
                    else:
                        break
            else:
                if ltree.dataArray[ltree.loserTree[0]].value > self.MINIMAX.value:
                    self.MINIMAX = ltree.dataArray[ltree.loserTree[0]]
                    self.tmp.append(self.MINIMAX.value)

                    if final:
                        ltree.dataArray[ltree.loserTree[0]] = self.rsnode()
                    else:
                        line = self.readline()
                        if line:
                            ltree.dataArray[ltree.loserTree[
                                0]] = self.rsnode(line)
                        else:
                            # 读到头了
                            break
                else:
                    ltree.dataArray[ltree.loserTree[0]].rowNum += 1
        # And don't forget self.tmp. If self.tmp is not empty, write it into
        # file.
        if final and self.tmp:
            self.writetmp(self.nfilename(self.sonfileNum))

    def splitFile(self):
        """
        split large file into sorted son files.
        """
        ltree = LoserTree(self.n)
        line = self.readline()
        if line == None:
            return
        for i in range(self.n):
            ltree.dataArray[i] = RSNode(1, line)
            ltree.adjust(i)
            line = self.readline()
        self.sonfileNum = 1
        self.MINIMAX = ltree.dataArray[ltree.loserTree[0]]
        self.tmp = [self.MINIMAX.value]

        self.replace_selection(ltree, line)
        self.replace_selection(ltree, line, final=True)
        self.fr.close()

    def merge_file(self, filenames, newname):
        """
        merge files into a new file.
        """
        frs = [open(filename, 'r') for filename in filenames]
        minfr = None
        n = len(filenames)
        fw = open(newname, 'w')
        ltree = LoserTree(n)
        lines = []
        for ind, fr in enumerate(frs):
            line = fr.readline()
            lines.append(line)
            ltree.dataArray[ind] = RSNode(1, line, ind)
            ltree.adjust(ind)
        while True:
            minmax = ltree.dataArray[ltree.loserTree[0]]
            minfr_ind = minmax.freader_ind
            # print "before data:{}".format([i.value for i in ltree.dataArray])
            # print("minfr_ind:{}".format(minfr_ind))
            fw.write(minmax.value)
            lines[minfr_ind] = frs[minfr_ind].readline()
            if lines.count("") == n:
                break
            line = lines[minfr_ind]
            if line != "":
                ltree.dataArray[minfr_ind] = RSNode(1, line, minfr_ind)
                ltree.adjust(minfr_ind)
            else:
                ltree.dataArray[minfr_ind] = RSNode(1, (1, 1), minfr_ind)
                ltree.adjust(minfr_ind)
            # print("line:{}".format(line))
            # print "after data:{}".format([i.value for i in ltree.dataArray])
            # raw_input()

        # print "left data:{}".format([i.value for i in ltree.dataArray])

        for ind, fr in enumerate(frs):
            fr.close()
            os.remove(filenames[ind])
        fw.close()

    def merge(self, k=3):
        """k-huffman merge"""
        print("total num: {}".format(self.NUM_FILE))
        merge_num = 0
        while len(self.sizes) != 1:
            merge_num += 1
            sorted_sizes = sorted(self.sizes.items(), key=lambda t: t[1])
            filenames = []
            newname = os.path.join(self.tarDir, '{}-merge-{}.txt'.format(
                os.path.basename(os.path.splitext(self.LargeFile)[0]), merge_num))
            # print "sizes:{}".format(self.sizes)
            for i in range(k):
                if i < len(sorted_sizes): # don't have enough files.
                    filename = sorted_sizes[i][0]
                    filenames.append(filename)
                    self.sizes[newname] += self.sizes[filename]
                    self.sizes.pop(filename)
            # print "filenames:{}, newname:{}".format(filenames, newname)
            self.merge_file(filenames, newname)
        print("result total num: {}".format(self.sizes[newname]))
        os.rename(newname, os.path.join(self.tarDir, "result.txt"))


if __name__ == '__main__':
    try:
        LargeFile = sys.argv[1]
        tarDir = sys.argv[2]
        n = int(sys.argv[3])
    except Exception as e:
        print("error: {}".format(e))
        print("""Usage: you need input 3 parameters.
            1. path of LargeFile.
            2. target directory.
            3. size of loserTree.
            """)
        sys.exit(1)
    from time import ctime
    print("start time: {}".format(ctime()))
    slf = SortLargeFile(LargeFile, tarDir, n)
    slf.splitFile()
    slf.merge()
    print("  end time: {}".format(ctime()))
