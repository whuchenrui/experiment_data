# coding=utf-8
__author__ = 'ray'

import os
import sys
sys.path.append(r'../../')
from lib import Function
from lib.Config import Config
from FilterRule import FilterRule


"""
负责连接不同日期下的序列，过滤全为0的序列. 并统计出三个删除条件(过长序列, 连1过长, 1占比过多) 对应的数据值
count_seq_info()  统计出这些过滤数值
filter_data()  过滤不符合条件的数据
结果输出到 ranking_result_filter 文件夹下, 按照日期小时存储, 每条记录一行, 结构为{'idfa': idfa, 'pic': [],
    'result': [], 'act_time': []}
"""


def count_seq_info(st_time, end_time):
    """
    :param st_time:   开始日期
    :param end_time:   结束日期
    主要操作: 酸楚有效序列的最大长度, 有效序列的最多连续1个数, 有效序列中1占的最大比例, 用户操作时间分布
    并写入到data.conf文件
    :return:  总的序列长度
    """
    list_time = Function.get_time_list(st_time, end_time)
    cf = Config('data.conf')
    raw_data_path = cf.get('path', 'raw_data')
    percent_request_num = float(cf.get('filter_percent', 'request_num'))
    percent_sub_seq_length = float(cf.get('filter_percent', 'sub_seq_length'))
    percent_click_percent = float(cf.get('filter_percent', 'click_percent'))
    act_type = int(cf.get('act_type', 'value'))

    total = 0                                # 总的有效序列个数
    dict_request_distribution = {}           # 统计序列长度分布, 找出95%对应的序列长度值  {request: xx }
    dict_sub_seq_len_distribution = {}       # 统计序列1子序列长度分布                    {len: xx }
    dict_click_percent_distribution = {}     # 统计序列1占总体的比例分布                  {percent: xx }
    dict_act_time_distribution = {}          # 统计用户在每次请求上的停留时间 act_time 字段记录了request-1次的停留时间,
                                             # 下标与请求次数对应, 第一位为0, 无含义  {request: [user_num, total_time]}

    for day in list_time:
        input_path = raw_data_path + day
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in = input_path + '\\full_' + temp_name + str(i)
                if os.path.exists(file_in):
                    fin = open(file_in, 'r')
                    dict_file = eval(fin.read())
                    for idfa in dict_file:
                        list_result = dict_file[idfa]['result']
                        act_time = dict_file[idfa]['act_time']
                        click_num = 0
                        for r in list_result:
                            if r >= act_type:
                                click_num += 1
                        if click_num == 0:   # 删除全0, act_type为1,删除没有点击的序列, 为2删除没有save的序列
                            continue
                        length = len(list_result)
                        request = length/36
                        if request not in dict_request_distribution:  # 统计序列长度分布
                            dict_request_distribution[request] = 0
                        dict_request_distribution[request] += 1
                        temp_value = get_sub_seq_cnt(list_result, act_type, length)
                        if temp_value not in dict_sub_seq_len_distribution:  # 统计连续1的长度分布
                            dict_sub_seq_len_distribution[temp_value] = 0
                        dict_sub_seq_len_distribution[temp_value] += 1
                        temp_value = int(float(click_num)/length*100)
                        if temp_value not in dict_click_percent_distribution:
                            dict_click_percent_distribution[temp_value] = 0
                        dict_click_percent_distribution[temp_value] += 1
                        for j in range(1, request):    # 首位0无意义, 过滤
                            if j not in dict_act_time_distribution:
                                dict_act_time_distribution[j] = [0, 0]
                            dict_act_time_distribution[j][0] += 1
                            dict_act_time_distribution[j][1] += act_time[j]
                        total += 1
                    fin.close()
        print 'finish ', day

    preserve_request_num = int(total*percent_request_num)
    preserve_sub_seq_length = int(total*percent_sub_seq_length)
    preserve_click_percent = int(total*percent_click_percent)

    cf = Config('rule.conf')   # 写入过滤条件至rule.conf文件
    # 找出max_request_num
    length = len(dict_request_distribution)
    temp = 0
    for i in range(1, length+1):
        if temp < preserve_request_num:
            temp += dict_request_distribution[i]
        else:
            temp = i-1
            break
    cf.set('filter_value', 'max_request_num', str(temp))
    # end

    # 找出max_su_seq_length
    length = len(dict_sub_seq_len_distribution)
    temp = 0
    for i in range(1, length+1):
        if temp < preserve_sub_seq_length:
            temp += dict_sub_seq_len_distribution[i]
        else:
            temp = i-1
            break
    cf.set('filter_value', 'max_sub_seq_length', str(temp))
    # end

    # 找出max_click_percent
    length = len(dict_click_percent_distribution)
    temp = 0
    for i in range(0, length+1):
        if temp < preserve_click_percent:
            temp += dict_click_percent_distribution[i]
        else:
            temp = i-1
            break
    temp = round(float(temp)/100, 2)  # 转换为小数
    cf.set('filter_value', 'max_click_percent', str(temp))
    # end

    # 计算出用户每次请求停留时间分布
    length = len(dict_act_time_distribution)
    temp = ''
    list_average_time = []
    for i in range(1, length+1):
        total_seq = dict_act_time_distribution[i][0]
        total_time = dict_act_time_distribution[i][1]
        average_time = round(float(total_time)/total_seq, 1)
        temp += str(average_time) + ','
        list_average_time.append([i, average_time])
    temp.strip(',')
    cf.set('filter_value', 'act_time', temp)
    # end
    cf.write()          # 执行写入
    return total


def filter_data(time_st, time_end):
    list_time = Function.get_time_list(time_st, time_end)
    cf = Config('data.conf')
    raw_data_path = cf.get('path', 'raw_data')
    filter_data_output = cf.get('path', 'position_bias_data')
    act_type = int(cf.get('act_type', 'value'))
    filer_rule = FilterRule('rule.conf', act_type)   # 初始化处理过滤的类 FilterRule
    valid_cnt = 0
    invalid = 0

    for day in list_time:
        input_path = raw_data_path + day
        output_path = filter_data_output + day
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in = input_path + '\\full_' + temp_name + str(i)
                if os.path.exists(file_in):
                    file_pic = output_path + '\\pic_' + temp_name + str(i)
                    file_result = output_path + '\\result_' + temp_name + str(i)
                    fout_pic = open(file_pic, 'w')
                    fout_result = open(file_result, 'w')

                    fin = open(file_in, 'r')
                    dict_file = eval(fin.read())
                    for idfa in dict_file:
                        list_pic = dict_file[idfa]['pic']
                        list_result = dict_file[idfa]['result']
                        length = len(list_result)
                        length_pic = len(list_pic)
                        if length_pic != length:
                            print 'result number overflow the ranking!'
                            continue
                        act_time = dict_file[idfa]['act_time']
                        is_valid = filer_rule.check_each_seq(list_result)
                        if is_valid:
                            out_pic = ''
                            out_result = ''
                            for j in range(0, length):
                                out_pic += list_pic[j] + ' '
                                out_result += str(list_result[j]) + ' '
                            out_pic.strip(' ')
                            out_result.strip(' ')
                            fout_pic.write(out_pic + '\n')
                            fout_result.write(out_result + '\n')
                            valid_cnt += 1
                        else:
                            invalid += 1
                    fin.close()
                    fout_pic.close()
                    fout_result.close()
        print 'filter ', day
    return valid_cnt


def get_click_cnt(line, value):
    cnt = 0
    for item in line:
        if item >= value:
            cnt += 1
    return cnt


def get_sub_seq_cnt(line, value, length):
    c_len = 0               # 当前最长1序列长度
    max_len = 0             # 最大1序列长度
    for i in range(0, length):
        if line[i] >= value:
            if c_len > 0:
                c_len += 1
            else:
                c_len = 1
        else:
            if c_len > max_len:
                max_len = c_len
            c_len = 0
    if c_len > max_len:    # 处理最后一个数字为1的情况
        max_len = c_len
    return max_len
