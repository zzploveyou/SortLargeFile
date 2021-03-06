﻿# SortLargeFile


## 1. 置换选择排序算法

假设初始待排文件为输入文件FI, 初始归并段文件为输出文件FO,
内存工作区为WA, FO和WA的初始状态为空, 并设内存工作区WA的容量为w个记录,
则置换-选择排序的操作过程为：
1. 从FI输入w个记录到工作区WA;
2. 从WA中选出其中关键字最小值的记录, 记为MINIMAX记录；
3. 将MINIMAX记录输出到FO中去；
4. 若FI不空, 则从FI输入下一个记录到WA中；
5. 从WA中所有关键字比MINIMAX记录的关键字大的记录中选出最小关键字记录,
作为新的MINIMAX记录；
6. 重复3-5, 直至在WA中选不出新的MINIMAX记录为止, 由此得到一个初始归并段,
输出一个归并段的结束标志到FO中去；
7. 重复2-6, 直至WA为空, 由此得到全部初始归并段。

在WA中选择MINIMAX记录的过程需利用“败者树”来实现。
1. 内存工作区中的记录作为败者树的外部节点，
而败者树的根节点的父节点指示工作区中关键字最小的纪录；
2. 为了便于选出MINIMAX记录，为每一个记录附设一个所在归并段的序号，
在进行关键字的比较时，现比较段号，段号小的为胜者，段号相同的则关键字小的为胜者；
3. 败者树的建立可从设工作区中所有记录的段号均为“0”开始，
然后从FI逐个输入w个记录到工作区是，自下而上调整败者树，
由于这些记录的段号为“1”，则他们对于“0”段的记录而言均为败者，
从而逐个填充到败者树的各节点中去。

## 2. k路huffman平衡归并
对n个归并段, 以长度作为权重,构建huffman树, 并利用败者树进行归并排序.


## 3. 最终测试时间结果

|行数|时间(s)|
|:-:|:-:|
100000|2
200000|3
400000|7
800000|14
1600000|29
3200000|63



