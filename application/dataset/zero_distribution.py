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


def get_click_num(list_seq):
    num = 0
    for i in range(0, len(list_seq)):
        if list_seq[i] > 0:
            num += 1
    return num


def exec_distribution(_time1, _time2):
    list_time = get_time_list(_time1, _time2)
    cf = ConfigParser()
    cf.read('..\\..\\config\\data.conf')
    data_path = cf.get('file', 'path')
    source_path = cf.get('dataset', 'path')
    chart_path = cf.get('dataset', 'chart')
    dict_distribution = {}

    for time in list_time:
        current_path = data_path + time
        if os.path.exists(current_path):
            for i in range(0, 24):
                file_path = current_path + '\\'
                hour = ''
                if i < 10:
                    hour = '0'
                hour += str(i)
                result_name = file_path+'result_' + hour
                if os.path.exists(result_name):
                    file_time = time + ':' + hour
                    if file_time not in dict_distribution:
                        dict_distribution[file_time] = {}
                    seq_zero_num = 0
                    seq_total_num = 0
                    seq_zero_pic_num = 0
                    seq_total_pic_num = 0
                    seq_total_click_num = 0
                    fin_result = codecs.open(result_name, 'r', encoding='utf-8')
                    while True:
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').split(' ')
                        seq_length = len(list_result)
                        temp = 0
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                            if list_result[index] > 0:
                                temp += 1
                        if temp == 0:
                            seq_zero_pic_num += seq_length
                            seq_zero_num += 1
                        seq_total_num += 1
                        seq_total_pic_num += seq_length
                        seq_total_click_num += temp
                    dict_distribution[file_time]['seq_zero_num'] = seq_zero_num
                    dict_distribution[file_time]['seq_total_num'] = seq_total_num
                    dict_distribution[file_time]['seq_zero_pic_num'] = seq_zero_pic_num
                    dict_distribution[file_time]['seq_total_pic_num'] = seq_total_pic_num
                    dict_distribution[file_time]['seq_total_click_num'] = seq_total_click_num
                    fin_result.close()
                print str(i), len(dict_distribution)

    fout_result = open(source_path+'seq_distribution_raw', 'w')
    fout_result.write(str(dict_distribution))
    fout_result.close()


def print_format_distribution():
    cf = ConfigParser()
    cf.read('..\\..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_path = cf.get('dataset', 'chart')
    fin = open(source_path+'seq_distribution_raw', 'r')
    line = fin.read()
    dict_raw = eval(line)
    list_zero_num_column = []
    list_total_num_column = []
    list_probability = []
    for day in range(4, 24):
        if day < 10:
            full_day = '0' + str(day)
        else:
            full_day = str(day)
        for hour in range(0, 24):
            if hour < 10:
                full_hour = '0' + str(hour)
            else:
                full_hour = str(hour)
            time = '2014-11-'+full_day+':'+full_hour
            if time not in dict_raw:
                continue
            format_time = strptime(time, "%Y-%m-%d:%H")
            highcharts_utc_time = (mktime(format_time) + 8*3600)*1000
            list_zero_num_column.append([highcharts_utc_time, dict_raw[time]['seq_zero_num']])
            list_total_num_column.append([highcharts_utc_time, dict_raw[time]['seq_total_num']])
            temp_value = float(dict_raw[time]['seq_zero_num'])/dict_raw[time]['seq_total_num']
            list_probability.append([highcharts_utc_time, round(temp_value, 3)])
    fout = open(chart_path+'distribution_result', 'w')
    fout.write('zero_column\n')
    fout.write(str(list_zero_num_column))
    fout.write('\n\ntotal_column\n')
    fout.write(str(list_total_num_column))
    fout.write('\n\nline\n')
    fout.write(str(list_probability))
    fout.close()
    fin.close()


def print_click_ratio():
    cf = ConfigParser()
    cf.read('..\\..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_path = cf.get('dataset', 'chart')
    fin = open(source_path+'seq_distribution_raw', 'r')
    line = fin.read()
    dict_raw = eval(line)
    list_total_pic_num = []
    list_total_click_num = []
    list_probability_with_zero = []
    list_ratio_zero_and_total = []
    for day in range(4, 24):
        if day < 10:
            full_day = '0' + str(day)
        else:
            full_day = str(day)
        for hour in range(0, 24):
            if hour < 10:
                full_hour = '0' + str(hour)
            else:
                full_hour = str(hour)
            time = '2014-11-'+full_day+':'+full_hour
            if time not in dict_raw:
                continue
            format_time = strptime(time, "%Y-%m-%d:%H")
            highcharts_utc_time = (mktime(format_time) + 8*3600)*1000
            list_total_pic_num.append([highcharts_utc_time, dict_raw[time]['seq_total_pic_num']])
            list_total_click_num.append([highcharts_utc_time, dict_raw[time]['seq_total_click_num']])
            temp_value = float(dict_raw[time]['seq_total_click_num'])/dict_raw[time]['seq_total_pic_num']
            list_probability_with_zero.append([highcharts_utc_time, round(temp_value, 3)])
            temp_value = float(dict_raw[time]['seq_zero_pic_num'])/dict_raw[time]['seq_total_pic_num']
            list_ratio_zero_and_total.append([highcharts_utc_time, round(temp_value, 3)])
    fout = open(chart_path+'click_ratio_result', 'w')
    fout.write('list_total_click_num\n')
    fout.write(str(list_total_click_num))
    fout.write('\n\nlist_total_pic_num\n')
    fout.write(str(list_total_pic_num))
    fout.write('\n\nlist_probability_with_zero\n')
    fout.write(str(list_probability_with_zero))
    fout.write('\n\nlist_ratio_zero_and_total\n')
    fout.write(str(list_ratio_zero_and_total))
    fout.close()
    fin.close()


if __name__ == '__main__':
    # exec_distribution('2014-11-03', '2014-11-24')
    # 1417651200000  1417654800000  1417658400000
    print_click_ratio()
