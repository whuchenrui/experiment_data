# coding=utf-8
__author__ = 'CRay'

import codecs


# 计算不同长度的序列总的点击次数
def exec_folder():
    dict_seq_click = {}
    fin = codecs.open('result_new', 'r', encoding='UTF-8')
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.split(' ')
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        length = len(list_res)
        request = length/36
        if request not in dict_seq_click:
            dict_seq_click[request] = {'click': 0, 'num': 0}
        click_num = 0
        for i in range(0, length):
            if list_res[i] > 0:
                click_num += 1
        dict_seq_click[request]['num'] += 1
        dict_seq_click[request]['click'] += click_num
    fin.close()
    print 'last: ', dict_seq_click


if __name__ == '__main__':
    exec_folder()