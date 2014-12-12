# coding=utf-8
__author__ = 'CRay'
import codecs
from ConfigParser import ConfigParser
import traceback

def turn_probability(_type, min_req, max_req, max_click, back_st, back_end):
    """
    _type: save or view
    min_seq:    用于统计的最短序列
    max_seq:    用于统计的最长序列
    max_click:  统计最多点击多少图片
    back_st:    统计范围的起始处
    back_end:   统计范围的终点处
    {req1: {0: [a. b], 1: [a, b]}} req1: seq长度，0: 最后K页点击的图片数量 a没向后翻看的人: b:向后翻的人数
    probability = (b)/(a+b)
    """
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    action = int(cf.get('type', 'type'))

    #TODO： 此处要修改， else 的默认为 result
    if _type == 'save':
        name = 'result_raw'
    else:
        name = 'result_raw'

    fin_result = codecs.open(source_path+name, 'r', encoding='UTF-8')
    dict_result = {}
    for i in range(min_req, max_req+1):
        dict_result[i] = {}
    while True:
        line = fin_result.readline()
        if not line:
            break
        result = line.strip('\n').split(' ')
        length = len(result)
        request = length/36
        if request < min_req:
            continue
        for index, item in enumerate(result):
            result[index] = int(item)
        if request > max_req:
            request = max_req+1
        for req in range(min_req, request):
            start = (req - back_st) * 36
            end = (req - back_end) * 36
            count = 0
            for i in range(start, end):
                if result[i] >= action:
                    count += 1
            if count not in dict_result[req]:
                dict_result[req][count] = [0, 0]
            dict_result[req][count][1] += 1
        if request <= max_req:
            start = (request - back_st) * 36
            end = (request - back_end) * 36
            count = 0
            for i in range(start, end):
                if result[i] >= action:
                    count += 1
            if count not in dict_result[request]:
                dict_result[request][count] = [0, 0]
            dict_result[request][count][0] += 1
    print dict_result
    fin_result.close()
    file_name = 'turn_probability_start_' + str(back_st) + '_end_' + str(back_end) + '.log'

    # print
    fout = codecs.open(chart_data+file_name, 'w', encoding='UTF-8')
    for req in dict_result:
        a = []
        for i in range(0, max_click+1):
            if i in dict_result[req]:
                if dict_result[req][i][1] == 0:
                    a.append([i, 0])
                else:
                    temp = float(dict_result[req][i][1])/(dict_result[req][i][1]+dict_result[req][i][0])
                    a.append([i, round(temp, 3)])
            else:
                print str(i) + 'is not in request: ' + str(req)
        fout.write("{ name: 'request= " + str(req) + "', data: ")
        fout.write(str(a))
        fout.write('}, \n')
    fout.close()