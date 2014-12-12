# coding=utf-8
__author__ = 'CRay'

import codecs


def forget(_req):
    print _req
    fin = codecs.open('result_09_new', 'r', encoding='UTF-8')
    dict_result = {}  # {0: [1, 2]}  key: 开始处点击的情况   list值[向后翻页的数量, 开始处点key次的数量]
    while True:
        line = fin.readline()
        if not line:
            break
        result = line.strip('\n').split(' ')
        length = len(result)
        is_turn = False              # 请求request次后是否继续往后翻
        if length/36 < request:
            continue
        elif length/36 > request:
            is_turn = True
        for index, item in enumerate(result):
            result[index] = int(item)
        count = 0
        for i in range((_req-1)*36, _req*36):  # 计算指定请求的点击情况
            if result[i] > 0:
                count += 1
        if count not in dict_result:
            dict_result[count] = [0, 0]
        if is_turn:
            dict_result[count][0] += 1
        dict_result[count][1] += 1
    print_result(dict_result)
    fin.close()


def print_result(dict_result):
    a = []
    for i in range(0, 10):
        temp = []
        temp.append(i)
        if i not in dict_result:
            temp.append(0)
        else:
            probability = round(float(dict_result[i][0])/dict_result[i][1], 3)
            temp.append(probability)
        a.append(temp)
    print a
    print dict_result
    print


if __name__ == '__main__':
    request = 10             # 选定某长度的seq
    # last_num = 2          # 最后N次请求操作相似的seq
    # last_same_num = 3     # 最后N次请求中点开K张图片
    # first_num = 1         # 最开始N次请求中操作差异非常大的seq
    for req in range(1, request):
        forget(req)