# coding=utf-8
__author__ = 'CRay'
import os
from lib.Config import Config
from lib import Function


def turn_probability(st_time, end_time, behavior, min_page, max_page, back_st, back_end, max_click):
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
    dict_distribution = {}
    for i in range(min_page, max_page+1):
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
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        not_null_position = 0
                        for m in range(length-1, length-28, -1):  # 仅考虑最后3页情况
                            if list_result[m] >= 1:
                                not_null_position = m
                                break
                        if not_null_position == 0:
                            not_null_position = length - 28
                        not_null_position += 1   # 数组从0开始计数, 为了方便计算页码, 这里加1处理
                        if not_null_position % 9 == 0:
                            page_num = not_null_position/9
                        else:
                            page_num = not_null_position/9 + 1
                        dict_distribution.setdefault(page_num, 0)
                        dict_distribution[page_num] += 1
                        if page_num < min_page:
                            continue
                        if page_num > max_page:
                            page_num = max_page + 1
                        for page in range(min_page, page_num):  # 这里req<request, 不能等于
                            start = (page - back_st) * 9
                            end = (page - back_end) * 9
                            click_num = 0
                            for j in range(start, end):
                                if list_result[j] >= act_value:
                                    click_num += 1
                            dict_result[page].setdefault(click_num, [0, 0])
                            dict_result[page][click_num][1] += 1
                        # 统计序列最后一次操作情况, 当序列超过统计长度, 则他在指定范围内的所有操作都视为翻页
                        if page_num <= max_page:
                            start = (page_num - back_st) * 9
                            end = (page_num - back_end) * 9
                            click_num = 0
                            for j in range(start, end):
                                if list_result[j] >= act_value:
                                    click_num += 1
                            dict_result[page_num].setdefault(click_num, [0, 0])
                            dict_result[page_num][click_num][0] += 1
                    fin_result.close()
        print 'turn probability:  ', day
    list_distribution = []
    for p in dict_distribution:
        num = dict_distribution[p]
        list_distribution.append([p, num])
    list_distribution.sort(key=lambda x: x[0])
    print list_distribution
    # print
    file_name = '6-turn-probability-start-' + str(back_st) + '-end-' + str(back_end) + '-' + behavior + '.result'
    fout = open(chart_path+file_name, 'w')
    for page in dict_result:
        a = []
        for i in range(0, max_click+1):
            if i in dict_result[page]:
                temp = float(dict_result[page][i][1])/(dict_result[page][i][1]+dict_result[page][i][0])
                a.append([i, round(temp, 3)])
            else:
                print str(i) + 'is not in request: ' + str(page)
        fout.write("{ 'name': 'page= " + str(page) + "', 'data': ")
        fout.write(str(a))
        fout.write('}, \n')
    fout.close()

if __name__ == '__main__':
    # turn_probability('2014-11-04', '2014-11-08', 'all', 8, 60, 4, 0, 18)
    list_data = [[1, 1047], [2, 528], [3, 505], [4, 680], [5, 38275], [6, 1484], [7, 1751], [8, 2027], [9, 15503], [10, 190], [11, 210], [12, 243], [13, 12847], [14, 138], [15, 100], [16, 119], [17, 9088], [18, 90], [19, 64], [20, 63], [21, 9699], [22, 75], [23, 62], [24, 58], [25, 5855], [26, 30], [27, 28], [28, 35], [29, 7215], [30, 29], [31, 48], [32, 31], [33, 4665], [34, 43], [35, 29], [36, 33], [37, 3568], [38, 23], [39, 18], [40, 15], [41, 4740], [42, 21], [43, 22], [44, 44], [45, 2804], [46, 15], [47, 12], [48, 13], [49, 3688], [50, 24], [51, 19], [52, 20], [53, 2110], [54, 10], [55, 5], [56, 17], [57, 3079], [58, 14], [59, 19], [60, 17], [61, 1638], [62, 10], [63, 9], [64, 7], [65, 2328], [66, 9], [67, 11], [68, 7], [69, 1298], [70, 4], [71, 7], [72, 1], [73, 1692], [74, 4], [75, 11], [76, 7], [77, 1101], [78, 7], [79, 11], [80, 4], [81, 1588], [82, 8], [83, 13], [84, 6], [85, 398], [86, 1], [87, 3], [89, 1164], [90, 2], [91, 7], [92, 8], [93, 856], [94, 2], [95, 5], [96, 1], [97, 562], [98, 4], [99, 4], [100, 4], [101, 821], [102, 7], [103, 9], [104, 5]]
    total = 0
    for page in list_data:
        total += page[1]
    left = total
    list_result = []
    for info in list_data:
        current_page = info[0]
        prob = 1 - float(info[1])/left
        left -= info[1]
        list_result.append([current_page, round(prob, 4)])
    print list_result