# coding=utf-8
__author__ = 'CRay'

import pymongo
import os
from lib import Function
from lib.Config import Config
"""
mongodb 中有三张表
表1: pic_click_info  {'pid': pic,  }
"""


def count_pic_info(st_time, end_time, min_show_num):
    cf_data = Config('data.conf')
    filter_data = cf_data.get('path', 'filter_data')
    dataset_path = cf_data.get('path', 'dataset_path')
    list_time = Function.get_time_list(st_time, end_time)

    dict_result = {}  # {pic: {'2014-11-04': {page: [show, click], page2: [show, click]}}}
    for day in list_time:
        input_path = filter_data + day
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in_pic = input_path + '\\pic_' + temp_name + str(i)
                file_in_result = input_path + '\\result_' + temp_name + str(i)
                if os.path.exists(file_in_result):
                    fin_pic = open(file_in_pic, 'r')
                    fin_result = open(file_in_result, 'r')
                    while True:
                        line_pic = fin_pic.readline()
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_pic = line_pic.strip('\n').strip(' ').split(' ')
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        length = len(list_result)
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        for j in range(0, length):
                            page = j/9 + 1
                            page = str(page)
                            picture = list_pic[j]
                            if picture not in dict_result:
                                dict_result[picture] = {}
                            if day not in dict_result[picture]:
                                dict_result[picture][day] = {}
                            if page not in dict_result[picture][day]:
                                dict_result[picture][day][page] = [0, 0]
                            if list_result[j] >= 1:
                                dict_result[picture][day][page][1] += 1
                            dict_result[picture][day][page][0] += 1
                    fin_pic.close()
                    fin_result.close()
        print 'pic info: ', day

    dict_output = {}
    for p in dict_result:
        if p not in dict_output:
            dict_output[p] = {}
        for day in dict_result[p]:
            if day not in dict_output:
                dict_output[p][day] = {}
            for page in dict_result[p][day]:
                page_info = dict_result[p][day][page]
                if page_info[0] < min_show_num:
                    continue
                if page not in dict_output[p][day]:
                    dict_output[p][day][page] = page_info

    fout = open(dataset_path+'pic_info', 'w')
    fout.write(str(dict_output))
    fout.close()


def init_mongodb_pic_info():
    """
    该函数只需要初始化数据库一次, 写入到kdd数据库中的 pic_click_info 表
    """
    cf_data = Config('data.conf')
    dataset_path = cf_data.get('path', 'dataset_path')
    client = pymongo.Connection()
    conn = client.kdd
    cpic_info = conn.pic_click_info
    fin = open(dataset_path+'pic_info', 'r')
    dict_raw = eval(fin.read())
    for pic in dict_raw:
        each_line = {}
        each_line['pid'] = pic
        for day in dict_raw[pic]:
            each_line[day] = dict_raw[pic][day]
        record = cpic_info.find({'pid': pic}, {'_id': 0})
        if record.count() == 0:
            cpic_info.insert(each_line)
        else:
            print '该图片的信息已存在!'
    fin.close()
    client.close()


def init_mongodb_hour_ranking():
    """
    该函数只需要初始化数据库一次, 写入到kdd数据库中的 hour_ranking 表
    """
    cf_data = Config('data.conf')
    dataset_path = cf_data.get('path', 'dataset_path')
    client = pymongo.Connection()
    conn = client.kdd
    cranking = conn.hour_ranking
    fin = open(dataset_path+'hour_ranking', 'r')
    while True:
        line = fin.readline()
        if not line:
            break
        ranking_time, ranking = line.strip('\n').split('\t')
        list_ranking = ranking.strip(' ').split(', ')
        record = cranking.find({'time': ranking_time}, {'_id': 0})
        if record.count() == 0:
            cranking.insert({'time': ranking_time, 'ranking': list_ranking})
        else:
            print '该小时的ranking已存在!'
    fin.close()
    client.close()


if __name__ == '__main__':
    init_mongodb_pic_info()