# coding=utf-8
__author__ = 'CRay'

import os
from lib import Function
from lib.Config import Config
from lib.Mongo import Mongo


def test_data_baseline_all(st_time, end_time):
    list_time = Function.get_time_list(st_time, end_time)
    mongo = Mongo('kdd', 'pic_click_info')
    list_pic_click = []
    list_pic_probability = []
    record = mongo.collection.find({}, {'_id': 0})
    if record.count() > 0:
        for r in record:
            pic = r['pid']
            click_num = 0
            show_num = 0
            for day in list_time:
                if day in r:
                    for page in r[day]:
                        click_num += r[day][page][1]
                        show_num += r[day][page][0]
            list_pic_click.append([click_num, pic])
            if show_num > 0:
                prob = float(click_num)/show_num
                list_pic_probability.append([round(prob, 4), pic])
            else:
                list_pic_probability.append([0, pic])
    else:
        print '记录数为0'
    mongo.close()
    print 'dict number: ', len(list_pic_click)
    list_pic_click.sort(key=lambda x: x[0], reverse=True)
    list_pic_probability.sort(key=lambda x: x[0], reverse=True)
    list_out_click = []
    list_out_prob = []
    for item in list_pic_click:
        list_out_click.append(item[1])
    for item in list_pic_probability:
        list_out_prob.append(item[1])
    return list_out_click, list_out_prob


def test_data_position_bias():
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    data_name = '1104-1111_data2_pb'
    fin = open(path+data_name+'.txt', 'r')
    line = fin.readline()
    list_pic = line.split(',')
    fin.close()
    print 'pb, 图片总数: ', len(list_pic)
    return list_pic


def test_data_full_model():
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    data_name = '1104-1111_data3_full_normal_turn'
    fin = open(path+data_name+'.txt', 'r')
    line = fin.readline()
    list_pic = line.split(',')
    fin.close()
    print 'full model, 图片总数: ', len(list_pic)
    data_name = data_name.split('data3')[1]
    return list_pic, data_name


def select_share_pic(list_click_num, list_prob, list_position_bias, list_full_model, init_number):
    """
    两种方法创建共同集合:
    1, 从4组ranking中选出前K个图片, 选出这些图片中共有的, 保留图片在每个ranking中的相对位置, 返回四个小集合的rank
    2, 从4组ranking中选出前K张图片, 然后全部作为共有图片集合的一部分, 返回这些图片的在每个ranking中的位置, 返回新rank
    """
    # 测试1
    rank_click = list_click_num[0: init_number]
    rank_prob = list_prob[0: init_number]
    rank_pb = list_position_bias[0: init_number]
    rank_full = list_full_model[0: init_number]
    intersection = set(rank_click) | set(rank_prob) | set(rank_pb) | set(rank_full)
    print 'intersection: ', str(len(intersection))
    temp_rank_click = []
    temp_rank_prob = []
    temp_rank_pb = []
    temp_rank_full = []
    for pic in intersection:
        if pic in list_click_num:
            index = list_click_num.index(pic)
            temp_rank_click.append([index, pic])
        if pic in list_prob:
            index = list_prob.index(pic)
            temp_rank_prob.append([index, pic])
        if pic in list_position_bias:
            index = list_position_bias.index(pic)
            temp_rank_pb.append([index, pic])
        if pic in list_full_model:
            index = list_full_model.index(pic)
            temp_rank_full.append([index, pic])
    temp_rank_click.sort(key=lambda x: x[0])
    temp_rank_prob.sort(key=lambda x: x[0])
    temp_rank_pb.sort(key=lambda x: x[0])
    temp_rank_full.sort(key=lambda x: x[0])
    new_rank_click = []
    new_rank_prob = []
    new_rank_pb = []
    new_rank_full = []
    for item in temp_rank_click:
        new_rank_click.append(item[1])
    for item in temp_rank_prob:
        new_rank_prob.append(item[1])
    for item in temp_rank_pb:
        new_rank_pb.append(item[1])
    for item in temp_rank_full:
        new_rank_full.append(item[1])
    if len(new_rank_click) == len(new_rank_prob) == len(new_rank_pb) == len(new_rank_full):
        # print new_rank_click
        # print new_rank_prob
        # print new_rank_pb
        # print new_rank_full
        print '集合大小: ', len(new_rank_click)
        return new_rank_click, new_rank_prob, new_rank_pb, new_rank_full
    else:
        print '集合不相等, ', str(len(new_rank_click)), str(len(new_rank_prob)), \
            str(len(new_rank_pb)), str(len(new_rank_full))


if __name__ == '__main__':
    # St_time = '2014-11-04'
    # End_time = '2014-11-06'
    # data3_full_raw = data_full_model(4000)
    # data2_pb, data3_full, pic_num = data_position_bias(data3_full_raw)
    # Pic_group_baseline = data_baseline(St_time, End_time, data2_pb)
    a = 5
    print a%5