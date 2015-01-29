# coding=utf-8
__author__ = 'ray'

import codecs
import os
from ConfigParser import ConfigParser
from datetime import datetime, timedelta


# 负责连接不同日期下的序列，制作dict存储图片出现的位置，点击情况并且记录小时信息。
# {{pic1: {1: [show_cnt, click_cnt, hour]}}}  pic1图片id，1表示出现的页码, hour 记录小时
# 参数为起止日期
def get_time_list(_timea, _timeb):
    timea = datetime.strptime(_timea, '%Y-%m-%d')
    timeb = datetime.strptime(_timeb, '%Y-%m-%d')
    time3 = timea
    time_len = (timeb - timea).days + 1
    num = 0
    list_time = list()
    while num < time_len:
        t3 = time3.strftime('%Y-%m-%d')
        time3 += timedelta(days=1)
        list_time.append(t3)
        num += 1
    return list_time


dict_pb_hour = {}   # 记录每个图片出现的位置和时间
dict_pb_hour_distribution = {}    # 记录点击概率与小时的关系

def get_sub_seq_cnt(line, action, length):
    c_len = 0               # 当前最长1序列长度
    max_len = 0             # 最大1序列长度
    for i in range(0, length):
        if line[i] >= action:
            if c_len > 0:
                c_len += 1
            else:
                c_len = 1
        else:
            if c_len > max_len:
                max_len = c_len
            c_len = 0
    if c_len > max_len:   # 处理最后一个数字为1的情况
        max_len = c_len
    return max_len


def exec_pb_hour(list_pic, list_result, file_time, length):
    for j in range(0, length):
        page = j/9 + 1
        picture = list_pic[j]
        if picture not in dict_pb_hour:
            dict_pb_hour[picture] = {}
        if page not in dict_pb_hour[picture]:
            dict_pb_hour[picture][page] = [0, 0, file_time]
        if file_time not in dict_pb_hour[picture][page][2]:
            dict_pb_hour[picture][page][2] += ',' + file_time
        if list_result[j] > 0:
            dict_pb_hour[picture][page][1] += 1
        dict_pb_hour[picture][page][0] += 1


def exec_pb_hour_distribution(list_result, hour):
    if hour not in dict_pb_hour_distribution:
        dict_pb_hour_distribution[hour] = [0, 0]
    for j in range(0, len(list_result)):
        if list_result[j] > 0:
            dict_pb_hour_distribution[hour][1] += 1
        dict_pb_hour_distribution[hour][0] += 1


def link_hour(time_st, time_end, min_page_num, max_request_num, max_sub_seq, max_sub_seq_ratio):
    list_time = get_time_list(time_st, time_end)
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    data_path = cf.get('file', 'path')
    source_path = cf.get('dataset', 'path')
    count = 0

    for time in list_time:
        current_path = data_path + time
        if os.path.exists(current_path):
            for i in range(0, 24):
                file_path = current_path + '\\'
                hour = ''
                if i < 10:
                    hour = '0'
                hour += str(i)
                pic_name = file_path+'pic_' + hour
                result_name = file_path+'result_' + hour
                if os.path.exists(pic_name):
                    file_time = time + ':' + hour
                    fin_pic = codecs.open(pic_name, 'r', encoding='utf-8')
                    fin_result = codecs.open(result_name, 'r', encoding='utf-8')
                    while True:
                        line_pic = fin_pic.readline()
                        line_result = fin_result.readline()
                        if not line_pic:
                            break
                        list_pic = line_pic.strip('\n').split(' ')
                        list_result = line_result.strip('\n').split(' ')
                        length = len(list_result)
                        if length > max_request_num * 36:
                            continue
                        click_num = 0
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                            if list_result[index] >= 1:
                                click_num += 1
                        if click_num == 0:
                            continue
                        sub_cnt_each_seq = get_sub_seq_cnt(list_result, 1, length)  # 每条序列, 1= view, length 序列长度
                        if sub_cnt_each_seq > max_sub_seq:
                            continue
                        if (float(sub_cnt_each_seq)/length) > max_sub_seq_ratio:
                            continue
                        count += 1
                        # exec_pb_hour 统计单张图片出现的页码和点击概率
                        exec_pb_hour(list_pic, list_result, file_time, length)
                        # exec_pb_hour_distribution 统计点击概率与小时的关系
                        exec_pb_hour_distribution(list_result, hour)
                    fin_pic.close()
                    fin_result.close()
                    print str(i)

    print '总的序列条数: ', count
    dict_output = {}
    for p in dict_pb_hour:
        if len(dict_pb_hour[p]) > min_page_num:
            dict_output[p] = dict_pb_hour[p]
    fout_result = open(source_path+'pic_position_hour', 'w')
    fout_result.write(str(dict_output))
    fout_result.close()

    list_output = []
    for j in range(0, 24):
        if j < 10:
            hour = '0' + str(j)
        else:
            hour = str(j)
        if hour not in dict_pb_hour_distribution:
            continue
        temp = float(dict_pb_hour_distribution[hour][1])/dict_pb_hour_distribution[hour][0]
        list_output.append([j, round(temp, 3)])
    fout_result = open(source_path+'pic_hour_distribution', 'w')
    fout_result.write(str(list_output))
    fout_result.close()

# if __name__ == '__main__':
#     link_hour('2014-10-26', '2014-10-31', 25, 5)