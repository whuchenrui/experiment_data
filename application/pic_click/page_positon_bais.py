# coding=utf-8
__author__ = 'CRay'

import codecs
from ConfigParser import ConfigParser


def position_bias(filter_req, _type):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    action = int(cf.get('type', 'type'))

    if _type == 'save':
        name = 'result_raw'
    else:
        name = 'result'
    fin_result = open(source_path+name, 'r')

    dict_result = {}  # {1: [show_num, click_num]}  show_num: 当前页码一共展示多少次图片，click_num，一共被点击量

    while True:
        line_result = fin_result.readline()
        if not line_result:
            break
        result = line_result.strip('\n').split(' ')
        length = len(result)
        requests = length/36
        if requests > filter_req:
            requests = filter_req
        for index, item in enumerate(result):
            result[index] = int(item)
        for i in range(1, 5):           # 统计前四页的呈现点击情况
            if i not in dict_result:
                dict_result[i] = [0, 0]
            dict_result[i][0] += 9
            for j in range((i-1)*9, i*9):
                if result[j] >= action:
                    dict_result[i][1] += 1
        for i in range(2, requests+1):
            page = i*4 - 3
            if page not in dict_result:
                dict_result[page] = [0, 0]
            dict_result[page][0] += 9
            for j in range((page-1)*9, page*9):
                if result[j] >= action:
                    dict_result[page][1] += 1
    fin_result.close()
    print_result(dict_result)


def print_result(result):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    chart_data = cf.get('dataset', 'chart')
    a = []  # column
    b = []  # probability per pic
    for page in result:
        a.append([page, result[page][0]])
        prob = float(result[page][1])/result[page][0]/9
        temp = round(prob, 4)
        b.append([page, temp])
    aa = []
    bb = []
    a.sort(key=lambda x: x[0])
    for item in a:
        aa.append(item[1])
    b.sort(key=lambda x: x[0])
    for item in b:
        bb.append(item[1])
    fout = open(chart_data+'4-position-bias.result', 'w')
    fout.write('column:\n')
    fout.write(str(aa))
    fout.write('\n\nline:\n')
    fout.write(str(bb))
    fout.close()