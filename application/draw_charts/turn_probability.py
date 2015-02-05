# coding=utf-8
__author__ = 'CRay'
import os
from lib.Config import Config
from lib import Function


def turn_probability(st_time, end_time, behavior, min_req, max_req, back_st, back_end, max_click):
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
    cf_data = Config('data.conf')
    fin_path = cf_data.get('path', 'filter_data')
    if 'all' == behavior:
        act_value = 1
        # fin_path = cf_data.get('path', 'filter_data')
    elif 'view' == behavior:
        act_value = 1
        # fin_path = cf_data.get('path', 'view_data')
    elif 'save' == behavior:
        act_value = 2
        # fin_path = cf_data.get('path', 'save_data')
    else:
        return False
    chart_path = cf_data.get('path', 'chart_result')

    list_time = Function.get_time_list(st_time, end_time)
    dict_result = {}
    for i in range(min_req, max_req+1):
        dict_result[i] = {}
    for day in list_time:
        input_path = fin_path + day
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in_result = input_path + '\\result_' + temp_name + str(i)
                if os.path.exists(file_in_result):
                    fin_result = open(file_in_result, 'r')
                    while True:
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        length = len(list_result)
                        request_num = length/36
                        if request_num < min_req:
                            continue
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        if request_num > max_req:
                            request_num = max_req + 1
                        for req in range(min_req, request_num):  # 这里req<request, 不能等于
                            start = (req - back_st) * 36
                            end = (req - back_end) * 36
                            click_num = 0
                            for j in range(start, end):
                                if list_result[j] >= act_value:
                                    click_num += 1
                            if click_num not in dict_result[req]:
                                dict_result[req][click_num] = [0, 0]
                            dict_result[req][click_num][1] += 1
                        # 统计序列最后一次操作情况
                        if request_num <= max_req:
                            start = (request_num - back_st) * 36
                            end = (request_num - back_end) * 36
                            click_num = 0
                            for j in range(start, end):
                                if list_result[j] >= act_value:
                                    click_num += 1
                            if click_num not in dict_result[request_num]:
                                dict_result[request_num][click_num] = [0, 0]
                            dict_result[request_num][click_num][0] += 1
                    fin_result.close()
        print 'turn probability:  ', day

    # print
    file_name = '6-turn-probability-start-' + str(back_st) + '-end-' + str(back_end) + '-' + behavior + '.result'
    fout = open(chart_path+file_name, 'w')
    for req in dict_result:
        a = []
        for i in range(0, max_click+1):
            if i in dict_result[req]:
                temp = float(dict_result[req][i][1])/(dict_result[req][i][1]+dict_result[req][i][0])
                a.append([i, round(temp, 3)])
            else:
                print str(i) + 'is not in request: ' + str(req)
        fout.write("{ name: 'request= " + str(req) + "', data: ")
        fout.write(str(a))
        fout.write('}, \n')
    fout.close()

if __name__ == '__main__':
    turn_probability('2014-11-04', '2014-12-14', 'all', 2, 12, 2, 0, 18)