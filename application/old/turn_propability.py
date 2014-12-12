# coding=utf-8
__author__ = 'CRay'

import codecs
import math
# 统计用户最后几页操作情况对翻页的影响


def turn_probability(file_name, func_type, target, value):
    target_cnt = 0    # 所有被记录的数据总和
    dict_turn = {}    # 点击指定数量继续向后翻的人数
    dict_total = {}   # 点击指定数量的总人数

    fin = codecs.open(file_name, 'r', encoding='utf-8')
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.split(' ')
        length = len(list_res)
        request = length/36
        if request < target:
            continue
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        target_cnt += 1
        cnt = 0
        if func_type == 1:
            # 所有页码
            start, end = 0, length
            cnt = 0
            for i in range(start, end):
                if list_res[i] > value:
                    cnt += 1

        elif func_type == 2:
            # 最后 4 页
            start, end = 36*(target-1), 36*target
            cnt = 0
            for i in range(start, end):
                if list_res[i] > value:
                    cnt += 1

        elif func_type == 3:
            # 最后6-3页/最后4页
            if request == target:
                start, end = 36*(target-1)-18, 36*target-18
            else:
                start, end = 36*(target-1), 36*target
            cnt = 0
            for i in range(start, end):
                if list_res[i] > value:
                    cnt += 1

        elif func_type == 4:
            # 最后8页
            start, end = 36*(target-2), 36*target
            cnt = 0
            for i in range(start, end):
                if list_res[i] > value:
                    cnt += 1

        elif func_type == 5:
            # forget 定值变化
            k = 2
            cnt = 0.0
            if request == target:
                temp = 0
                for i in range(0, 18):
                    if list_res[i] > value:
                        temp += 1
                division = math.pow(k, target-1)
                cnt += temp/division
                for i in range(1, target):
                    division = int(math.pow(k, target-i-1))
                    temp = 0
                    for j in range(36*(i-1)+18, 36*i+18):
                        if list_res[j] > value:
                            temp += 1
                    cnt += temp/division
            else:
                for i in range(1, target+1):
                    division = int(math.pow(k, target-i))
                    temp = 0
                    for j in range(36*(i-1), 36*i):
                        if list_res[j] > value:
                            temp += 1
                    cnt += temp/division

        cnt = int(cnt)
        if cnt not in dict_total:
            dict_total[cnt] = 0
        dict_total[cnt] += 1
        flag = False
        if request > target:
            flag = True
        if flag:
            if cnt not in dict_turn:
                dict_turn[cnt] = 0
            dict_turn[cnt] += 1
    fin.close()
    print dict_turn
    print dict_total
    print_data(dict_turn, dict_total, target_cnt)


def print_data(dict_turn, dict_total, target_cnt):
    a = []
    b = []
    for i in range(0, 40):
        if i not in dict_total:
            a.append(0)
        else:
            temp = round(float(dict_total[i])/target_cnt, 3)
            a.append(temp)

    for i in range(0, 40):
        if i not in dict_turn:
            b.append(0)
        else:
            temp = round(float(dict_turn[i])/dict_total[i], 3)
            b.append(temp)
    print '点击该数量图片的seq占总比例： ', a
    print '翻页概率： ', b
    print target_cnt


if __name__ == '__main__':
    #  1: {0, length}: 全部图片
    #  2: {36*(target-1), 36*target}: 最后四页
    #  3: {36*(target-1)-18, 36*target-18}: 最后6-最后3页
    #  4: {36*(target-2), 36*target}: 最后8页
    #  5: 每次请求按指数为2递减
    value = 1         # 0 没有点击  1点击  2save
    target = 6       # 考察请求次数
    func_type = 5
    file_name = 'result_09_new'
    turn_probability(file_name, func_type, target, value)