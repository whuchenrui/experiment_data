# coding=utf-8
__author__ = 'CRay'

import codecs
from ConfigParser import ConfigParser

def general_turn(_type):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')

    if _type == 'save':
        name = 'result_raw'
    else:
        name = 'result'

    fin_result = codecs.open(source_path+name, 'r', encoding='UTF-8')
    dict_result = {'total': 0}  # {1:x, 2:x, 'total': xx}} key: request  value: num,  total:总和
    while True:
        line_result = fin_result.readline()
        if not line_result:
            break
        result = line_result.strip('\n').split(' ')
        length = len(result)
        requests = length/36
        for index, item in enumerate(result):
            result[index] = int(item)
        if requests not in dict_result:
            dict_result[requests] = 0
        dict_result[requests] += 1
        dict_result['total'] += 1
    fin_result.close()
    print_result(dict_result)


def print_result(result):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    chart_data = cf.get('dataset', 'chart')
    length = len(result)
    output = []
    for i in range(1, length-1):
        temp = float(result['total']-result[i])/result['total']
        output.append([i, round(temp, 3)])
        result['total'] -= result[i]
    fout = codecs.open(chart_data+'general_turn.log', 'w', encoding='UTF-8')
    output_str = str(output)
    fout.write(output_str)
    fout.close()