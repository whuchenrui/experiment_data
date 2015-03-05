# coding=utf-8
__author__ = 'CRay'

import os
import sys
import traceback
sys.path.append(r'../../')
from lib import Function
from lib.Config import Config
from lib.Mongo import Mongo
"""
mongodb 中有三张表
表1: pic_click_info  {'pid': pic,  }
注意: 页码(page) 类型是string类型, 在使用字典读取时候需要注意
"""


def count_pic_info(st_time, end_time, min_show_num, behavior):
    cf_data = Config('data.conf')
    filter_data = cf_data.get('path', 'filter_data')
    dataset_path = cf_data.get('path', 'dataset_path')
    list_time = Function.get_time_list(st_time, end_time)

    # {pic: {'2014-11-04:02': [show, click, page]... }}  增加小时, key为日期+小时的组合
    dict_result = {}
    for day in list_time:
        input_path = filter_data + day
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                hour_info = temp_name + str(i)
                file_in_pic = input_path + '\\pic_' + hour_info
                file_in_result = input_path + '\\result_' + hour_info
                if os.path.exists(file_in_result):
                    fin_pic = open(file_in_pic, 'r')
                    fin_result = open(file_in_result, 'r')
                    full_time = day + ':' + hour_info
                    while True:
                        line_pic = fin_pic.readline()
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        if behavior == 'all':
                            pass
                        elif behavior == 'save':
                            if '2' not in line_result:
                                continue
                        elif behavior == 'click':
                            if '2' in line_result:
                                continue
                        list_pic = line_pic.strip('\n').strip(' ').split(' ')
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        length = len(list_result)
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        for j in range(0, length):
                            page = j/9 + 1
                            picture = list_pic[j]
                            if picture not in dict_result:
                                dict_result[picture] = {}
                            if full_time not in dict_result[picture]:
                                dict_result[picture][full_time] = [0, 0, 0, page]  # [show, click, save, page]
                            if list_result[j] >= 1:
                                dict_result[picture][full_time][1] += 1
                            if list_result[j] == 2:
                                dict_result[picture][full_time][2] += 1
                            dict_result[picture][full_time][0] += 1
                    fin_pic.close()
                    fin_result.close()
        print 'pic info ' + behavior + ': ', day

    dict_output = {}
    for p in dict_result:
        if p not in dict_output:
            dict_output[p] = {}
        for full_time in dict_result[p]:
            if dict_result[p][full_time][0] > min_show_num:
                if full_time not in dict_output[p]:
                    dict_output[p][full_time] = dict_result[p][full_time]
    fout = open(dataset_path+'pic_info_'+behavior, 'w')
    fout.write(str(dict_output))
    fout.close()


def init_mongodb_pic_info(behavior):
    """
    该函数只需要初始化数据库一次, 写入到kdd数据库中的 pic_click_behavior 表
    """
    cf_data = Config('data.conf')
    dataset_path = cf_data.get('path', 'dataset_path')
    if behavior == 'all':
        db_name = 'pic_info_all'
    elif behavior == 'save':
        db_name = 'pic_info_save'
    elif behavior == 'click':
        db_name = 'pic_info_click'
    else:
        return False
    mongo = Mongo('kdd', db_name)
    fin = open(dataset_path+db_name, 'r')
    dict_raw = eval(fin.read())  # 这里耗时最大, 文件比较大
    for pic in dict_raw:
        each_line = {}
        each_line['pid'] = pic
        for full_time in dict_raw[pic]:
            each_line[full_time] = dict_raw[pic][full_time]
        record = mongo.collection.find({'pid': pic}, {'_id': 0})
        if record.count() == 0:
            mongo.collection.insert(each_line)
        else:
            print '该图片的信息已存在!'
    fin.close()
    mongo.close()


def init_mongodb_hour_ranking():
    """
    该函数只需要初始化数据库一次, 写入到kdd数据库中的 hour_ranking 表
    """
    cf_data = Config('data.conf')
    dataset_path = cf_data.get('path', 'dataset_path')
    mongo = Mongo('kdd', 'hour_ranking')
    fin = open(dataset_path+'hour_ranking', 'r')
    while True:
        line = fin.readline()
        if not line:
            break
        ranking_time, ranking = line.strip('\n').split('\t')
        list_ranking = ranking.strip(' ').split(', ')
        record = mongo.collection.find({'time': ranking_time}, {'_id': 0})
        if record.count() == 0:
            mongo.collection.insert({'time': ranking_time, 'ranking': list_ranking})
        else:
            print '该小时的ranking已存在!'
    fin.close()
    mongo.close()


def init_group_pic_pb():
    """
    该函数只需要初始化数据库一次, 写入到kdd数据库中的 group_pic_pb 表, 用于在线的图片组的position bias 查询
    """
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    mongo = Mongo('kdd', 'group_pic_pb')
    fin = open(path+'/group_pic_position_hour', 'r')
    while True:
        line = fin.readline()
        if not line:
            break
        # linux 中处理windows文件的行, 需要去除'\r\n', windows 中这样写也可以
        group_id, page_click_info = line.strip('\r\n').split('\t')
        record = mongo.collection.find({'gid': int(group_id)}, {'_id': 0})
        page_click_info = eval(page_click_info)
        if record.count() == 0:
            mongo.collection.insert({'gid': int(group_id), 'pinfo': page_click_info})
        else:
            print str(group_id), ' 已存在 '
    fin.close()
    mongo.close()


if __name__ == '__main__':
    # count_pic_info('2014-11-04', '2014-12-14', 50)
    # init_mongodb_pic_info()
    # init_mongodb_hour_ranking()
    # init_group_pic_pb()
    # count_pic_info('2014-11-04', '2014-12-14', 0, 'all')
    # count_pic_info('2014-11-04', '2014-12-14', 0, 'click')
    # count_pic_info('2014-11-04', '2014-12-14', 0, 'save')
    # init_mongodb_pic_info('all')
    # init_mongodb_pic_info('click')
    # init_mongodb_pic_info('save')
    try:
        init_group_pic_pb()
    except:
        print traceback.format_exc()