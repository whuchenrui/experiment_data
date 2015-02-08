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


def data_position_bias(list_full_model):
    """
    k: 表示选择多少图片
    仅考虑position bias效应后的图片排序, 按照图片质量由高到低排序
    返回拥有共同集合的  pb, full 两个策略的排序, 并且返回图片个数(valid_num)
    """
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fin = open(path+'1104-1106_data2_pb.txt', 'r')
    line = fin.readline()
    list_pb_pic = line.split(',')
    fin.close()

    valid_num = 0
    list_pb_output = []
    list_full_output = []
    for pic in list_full_model:
        if pic in list_pb_pic:
            index_pb = list_pb_pic.index(pic)
            list_pb_output.append([index_pb, pic])
            index_full = list_full_model.index(pic)
            list_full_output.append([index_full, pic])
            valid_num += 1
    list_pb_output.sort(key=lambda x: x[0])
    pb = []
    full = []
    for item in list_pb_output:
        pb.append(item[1])
    for item in list_full_output:
        full.append(item[1])
    print '有效图片数: ', valid_num
    return pb, full, valid_num


def data_full_model(k):
    """
    考虑position bias效应, 并且考虑joy boredom 因素
    """
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    data_name = '1104-1106_data3_full_normal_turn'
    fin = open(path+data_name+'.txt', 'r')
    line = fin.readline()
    list_pic = line.split(',')
    print 'full model, 图片总数: ', len(list_pic)
    list_output = list_pic[0: k]
    fin.close()
    data_name = data_name.split('data3')[1]
    return list_output, data_name


if __name__ == '__main__':
    # St_time = '2014-11-04'
    # End_time = '2014-11-06'
    data3_full_raw = data_full_model(4000)
    data2_pb, data3_full, pic_num = data_position_bias(data3_full_raw)
    # Pic_group_baseline = data_baseline(St_time, End_time, data2_pb)
