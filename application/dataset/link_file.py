# coding=utf-8
__author__ = 'ray'

import codecs
import os
from ConfigParser import ConfigParser
from datetime import datetime, timedelta


# 负责连接不同日期下的序列，集合到pic，result两个文件中
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


def link(_time1, _time2):
    list_time = get_time_list(_time1, _time2)
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    data_path = cf.get('file', 'path')
    source_path = cf.get('dataset', 'path')
    long_percent = float(cf.get('percent', 'long_percent'))
    fout_pic = codecs.open(source_path+'pic_raw', 'a', encoding='UTF-8')
    fout_result = codecs.open(source_path+'result_raw', 'a', encoding='UTF-8')
    count = 0
    dict_distribution = {}
    for time in list_time:
        current_path = data_path + time
        if os.path.exists(current_path):
            # link pic
            for i in range(0, 24):
                file_path = current_path + '\\'
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_pic = file_path+'pic_'+temp_name+str(i)
                file_result = file_path+'result_'+temp_name+str(i)
                if os.path.exists(file_pic) and os.path.exists(file_result):
                    fin_pic = open(file_pic, 'r')
                    fin_result = open(file_result, 'r')
                    while True:
                        line_pic = fin_pic.readline()
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        if '1' not in line_result:
                            if '2' not in line_result:
                                continue
                        list_result = line_result.strip('\n').split(' ')
                        request = len(list_result)/36
                        if request not in dict_distribution:
                            dict_distribution[request] = 0
                        dict_distribution[request] += 1
                        fout_pic.write(line_pic)
                        fout_result.write(line_result)
                        count += 1
                    fin_pic.close()
                    fin_result.close()
    fout_pic.close()
    fout_result.close()

    percent_ninety_five = int(count*long_percent)  # 过滤序列过长的用户，过滤这3%的人
    request_num = len(dict_distribution)
    temp = 0
    for i in range(1, request_num+1):
        if temp < percent_ninety_five:
            temp += dict_distribution[i]
        else:
            temp = i-1
            break
    return count, temp
