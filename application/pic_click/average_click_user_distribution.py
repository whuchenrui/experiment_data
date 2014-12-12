# coding=utf-8
__author__ = 'CRay'

import codecs
from ConfigParser import ConfigParser

# 统计某一固定请求次数的序列在每页上的平均操作次数 和 去除1的子串后各个长度请求的分布图


def average_click(filter_req, _type):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    action = int(cf.get('type', 'type'))

    if _type == 'save':
        name = 'result_raw'
    else:
        name = 'result_1'

    fin = codecs.open(source_path+name, 'r', encoding='utf-8')
    dict_seq = {}
    for i in range(1, filter_req+1):
        dict_seq[i] = {}
    for req in dict_seq:
        dict_seq[req]['num'] = 0
        for i in range(1, req+1):
            dict_seq[req][i] = 0
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.strip('\n').split(' ')
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        length = len(list_res)
        req = length/36
        if req not in dict_seq:
            continue
        dict_seq[req]['num'] += 1
        for i in range(1, req+1):
            for j in range(36*(i-1), 36*i):
                if list_res[j] >= action:
                    dict_seq[req][i] += 1
    fin.close()
    print_result(dict_seq)


def print_result(result):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    chart_data = cf.get('dataset', 'chart')
    fout = codecs.open(chart_data+'average_click.log', 'w', encoding='utf-8')
    for req in result:
        a = []
        for i in range(1, req+1):
            if i not in result[req]:
                a.append([0, 0])
            if result[req]['num'] == 0:
                a.append([i, 0])
            else:
                average = round(float(result[req][i])/result[req]['num'], 3)
                a.append([i, average])
        fout.write("{ name: 'k= " + str(req) + "', data: ")
        fout.write(str(a))
        fout.write('}, \n')
    fout.close()


def distribution(_type):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    action = int(cf.get('type', 'type'))
    if _type == 'save':
        name = 'result_raw'
    else:
        # TODO: 依照情况修改这里的result_raw  和 result
        name = 'result_raw'  # 打开去除了1的子序列的log
    dict_result = {}
    count = 0
    fin = codecs.open(source_path+name, 'r', encoding='utf-8')
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.strip('\n').split(' ')
        count += 1
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        length = len(list_res)
        req = length/36
        if req not in dict_result:
            dict_result[req] = 0
        dict_result[req] += 1
    fin.close()
    print_distribution(dict_result, count)


def print_distribution(result, num):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    chart_data = cf.get('dataset', 'chart')
    fout = codecs.open(chart_data+'seq_distribution.log', 'w', encoding='utf-8')
    length = len(result)
    ratio = 1.0
    column = []
    line = []
    for i in range(1, length+1):
        if i not in result:
            column.append([0, 0])
            line.append([0, round(ratio, 3)])
        else:
            temp = round(float(result[i])/num, 3)
            column.append([i, temp])
            line.append([i, round(ratio, 3)])
            ratio -= temp
    fout.write('column: \n')
    fout.write(str(column))
    fout.write('\n\n line: \n')
    fout.write(str(line))
    fout.close()


# if __name__ == '__main__':
#     average_click()