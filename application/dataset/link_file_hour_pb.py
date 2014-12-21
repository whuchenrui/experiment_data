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


def link_hour(_time1, _time2, _filter_cnt, _min_page):
    list_time = get_time_list(_time1, _time2)
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    data_path = cf.get('file', 'path')
    source_path = cf.get('dataset', 'path')
    dict_pb_hour = {}
    _filter_cnt *= 36

    for time in list_time:
        current_path = data_path + time
        if os.path.exists(current_path):
            for i in range(0, 24):
                file_path = current_path + '\\'
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                pic_name = file_path+'pic_'+temp_name+str(i)
                result_name = file_path+'result_'+temp_name+str(i)
                if os.path.exists(pic_name):
                    file_hour = temp_name + str(i)
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
                        if length > _filter_cnt:
                            length = _filter_cnt
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        for j in range(0, length):
                            page = j/9 + 1
                            picture = list_pic[j]
                            if picture not in dict_pb_hour:
                                dict_pb_hour[picture] = {}
                            if page not in dict_pb_hour[picture]:
                                dict_pb_hour[picture][page] = [0, 0, file_hour]
                            if file_hour != dict_pb_hour[picture][page][2] and \
                                    len(file_hour) == len(dict_pb_hour[picture][page][2]):
                                dict_pb_hour[picture][page][2] += '_' + file_hour
                            elif file_hour not in dict_pb_hour[picture][page][2]:
                                dict_pb_hour[picture][page][2] += '_' + file_hour
                            if list_result[j] > 0:
                                dict_pb_hour[picture][page][1] += 1
                            dict_pb_hour[picture][page][0] += 1
                    fin_pic.close()
                    fin_result.close()
                    print str(i)

    dict_output = {}
    for p in dict_pb_hour:
        if len(dict_pb_hour[p]) > _min_page:
            dict_output[p] = dict_pb_hour[p]
    fout_result = codecs.open(source_path+'pic_position_hour', 'w', encoding='UTF-8')
    fout_result.write(str(dict_output))
    fout_result.close()


# if __name__ == '__main__':
#     link_hour('2014-10-26', '2014-10-31', 25, 5)