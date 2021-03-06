# coding=utf-8
__author__ = 'CRay'

import os
from lib.Config import Config
from lib import Function


def position_bias(st_time, end_time, behavior, max_req):
    """
    :param behavior:  all 整个过滤后数据集   view 不包含save操作的集合  save 包含save操作的集合
    :return:
    dict_result    {1: [show_num, click_num]}  show_num: 当前页码一共展示多少次图片，click_num，一共被点击量
    """
    cf_data = Config('data.conf')
    fin_path = cf_data.get('path', 'position_bias_data')
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
    # dict_result = {}  # {page: [show_num, click_num]}
    dict_result = {}    # {page: [show_num, click_num, save_num]} 增加纵坐标为 save/click
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
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        length = len(list_result)
                        request_num = length/36
                        if request_num > max_req:
                            continue
                        # page_num = request_num * 4
                        for j in range(1, 5):
                            if j not in dict_result:
                                dict_result[j] = [0, 0, 0]
                            dict_result[j][0] += 9
                            for k in range((j-1)*9, j*9):
                                if list_result[k] >= act_value:   # 这里统计点击情况
                                    dict_result[j][1] += 1
                                if list_result[k] == 2:
                                    dict_result[j][2] += 1
                        for j in range(2, request_num+1):
                            page = j*4 - 3
                            if page not in dict_result:
                                dict_result[page] = [0, 0, 0]
                            dict_result[page][0] += 9
                            for k in range((page-1)*9, page*9):
                                if list_result[k] >= act_value:
                                    dict_result[page][1] += 1
                                if list_result[k] == 2:
                                    dict_result[page][2] += 1
                    fin_result.close()
        print 'page pb: ', day

    ## 把dict_result按照格式输出, 画成highcharts图
    a1 = []  # 呈现数量
    a2 = []  # click数量
    a3 = []  # save数量
    b = []  # probability per page
    page_num = len(dict_result)*4
    for page in range(1, page_num):
        if page in dict_result:
            a1.append([page, dict_result[page][0]])
            a2.append([page, dict_result[page][1]])
            a3.append([page, dict_result[page][2]])
            prob = float(dict_result[page][2])/dict_result[page][0]  # 更改为save/show, 原始为 click/show
            temp = round(prob, 4)
            b.append([page, temp])
    fout = open(chart_path+'4-position-bias-'+behavior+'_Max-'+str(max_req)+'.result', 'w')
    fout.write('show number:\n')
    fout.write(str(a1))
    fout.write('\n\nclick number:\n')
    fout.write(str(a2))
    fout.write('\n\nsave number:\n')
    fout.write(str(a3))
    fout.write('\n\nsave/show:\n')
    fout.write(str(b))
    fout.close()


if __name__ == '__main__':
    position_bias('2014-11-04', '2014-12-14', 'all', 60)