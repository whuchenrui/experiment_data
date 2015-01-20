# coding=utf-8
__author__ = 'CRay'

import codecs
import os
from ConfigParser import ConfigParser
from datetime import datetime, timedelta
from time import *


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


def page_click_probability(_time1, _time2, max_request):
    list_time = get_time_list(_time1, _time2)
    cf = ConfigParser()
    cf.read('..\\..\\config\\data.conf')
    data_path = cf.get('file', 'path')
    source_path = cf.get('dataset', 'path')
    chart_path = cf.get('dataset', 'chart')
    dict_page_hour = {}
    dict_page_day = {}
    max_pic_num = max_request*36

    for day in list_time:
        current_path = data_path + day
        if os.path.exists(current_path):
            for i in range(0, 24):
                file_path = current_path + '\\'
                hour = ''
                if i < 10:
                    hour = '0'
                hour += str(i)
                result_name = file_path+'result_' + hour
                if os.path.exists(result_name):
                    if hour not in dict_page_hour:
                        dict_page_hour[hour] = {}
                    if day not in dict_page_day:
                        dict_page_day[day] = {}
                    fin_result = codecs.open(result_name, 'r', encoding='utf-8')
                    while True:
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').split(' ')
                        seq_length = len(list_result)
                        if seq_length > max_pic_num:  # 只统计固定页码内的情况
                            seq_length = max_pic_num
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        for page in range(1, (seq_length/9)+1):
                            if page not in dict_page_hour[hour]:
                                dict_page_hour[hour][page] = [0, 0]
                            if page not in dict_page_day[day]:
                                dict_page_day[day][page] = [0, 0]
                            temp_page_click_num = 0
                            for k in range(9*(page-1), 9*page):
                                if list_result[k] > 0:
                                    temp_page_click_num += 1
                            dict_page_hour[hour][page][0] += temp_page_click_num
                            dict_page_hour[hour][page][1] += 9
                            dict_page_day[day][page][0] += temp_page_click_num
                            dict_page_day[day][page][1] += 9
                    fin_result.close()
                print str(i), len(dict_page_hour), ' ', len(dict_page_day)

    fout_result = open(source_path+'page_hour_raw', 'w')
    fout_result.write(str(dict_page_hour))
    fout_result.close()

    fout_result = open(source_path+'page_day_raw', 'w')
    fout_result.write(str(dict_page_day))
    fout_result.close()


def print_page_hour_and_day():
    cf = ConfigParser()
    cf.read('..\\..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_path = cf.get('dataset', 'chart')
    fin = open(source_path+'page_hour_raw', 'r')
    dict_raw = eval(fin.read())
    list_output = []
    fout = open(chart_path+'page_hour_result', 'w')
    for i in range(0, 24):
        list_page_hour = []
        if i < 10:
            hour = '0' + str(i)
        else:
            hour = str(i)
        if hour not in dict_raw:
            continue
        for page in range(1, len(dict_raw[hour])-40):
            if page not in dict_raw[hour]:
                continue
            temp = float(dict_raw[hour][page][0])/dict_raw[hour][page][1]
            list_page_hour.append([page, round(temp, 3)])
        each_hour = {'name': hour, 'data': list_page_hour}
        list_output.append(each_hour)
    fout.write(str(list_output))
    fin.close()
    fout.close()

    fin = open(source_path+'page_day_raw', 'r')
    dict_raw = eval(fin.read())
    list_output = []
    fout = open(chart_path+'page_day_result', 'w')
    for i in range(3, 24):
        list_page_day = []
        if i < 10:
            day = '2014-11-0'+str(i)
        else:
            day = '2014-11-'+str(i)
        if day not in dict_raw:
            continue
        for page in range(1, len(dict_raw[day])-40):
            if page not in dict_raw[day]:
                continue
            temp = float(dict_raw[day][page][0])/dict_raw[day][page][1]
            list_page_day.append([page, round(temp, 3)])
        each_day = {'name': day, 'data': list_page_day}
        list_output.append(each_day)
    fout.write(str(list_output))
    fin.close()
    fout.close()


if __name__ == '__main__':
    # page_click_probability('2014-11-03', '2014-11-23', 25)
    print_page_hour_and_day()