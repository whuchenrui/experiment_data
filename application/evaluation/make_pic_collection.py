# coding=utf-8
__author__ = 'CRay'

import os
from lib import Function
from lib.Config import Config
from lib.Mongo import Mongo


def data_baseline(st_time, end_time, target_ranking):
    """
    baseline 数据集合, 共两个 图片为指定日期内
    1: 按照点击量排序的图片集合
    2: 按照平均点击概率排序的图片集合
    """
    list_time = Function.get_time_list(st_time, end_time)
    mongo = Mongo('kdd', 'pic_click_info')

    list_pic_click = []
    list_pic_probility = []
    for pic in target_ranking:
        record = mongo.collection.find({'pid': pic}, {'_id': 0})
        if record.count() > 0:
            show_num = 0
            click_num = 0
            record = record[0]
            for day in list_time:
                if day in record:
                    for page in record[day]:
                        click_num += record[day][page][1]  # [show, click] 所以这里是1
                        show_num += record[day][page][0]
            list_pic_click.append([click_num, pic])
            if show_num > 0:
                prob = float(click_num)/show_num
                list_pic_probility.append([round(prob, 4), pic])
            else:
                list_pic_probility.append([0, pic])
        else:
            print 'pis miss! ', pic
    mongo.close()

    list_pic_click.sort(key=lambda x: x[0], reverse=True)
    list_pic_probility.sort(key=lambda x: x[0], reverse=True)
    list_out_click = []
    list_out_prob = []
    for item in list_pic_click:
        list_out_click.append(item[1])
    for item in list_pic_probility:
        list_out_prob.append(item[1])
    return list_out_click, list_out_prob


def data_position_bias(k):
    """
    k: 表示选择多少图片
    仅考虑position bias效应后的图片排序, 按照图片质量由高到低排序
    """
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fin = open(path+'1107-1111-100-500.txt', 'r')
    line = fin.readline()
    list_pic = line.split(',')
    list_output = list_pic[0: k]
    fin.close()
    return list_output


def data_full_model():
    """
    考虑position bias效应, 并且考虑joy boredom 因素
    """
    pass


if __name__ == '__main__':
    St_time = '2014-11-04'
    End_time = '2014-11-06'
    Cf_data = Config('data.conf')
    path = Cf_data.get('path', 'dataset_path')
    Pic_group_position_bias = data_position_bias(1000)
    Pic_group_baseline = data_baseline(St_time, End_time, Pic_group_position_bias)
