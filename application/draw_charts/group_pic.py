# coding=utf-8
__author__ = 'CRay'

import codecs
import json
import traceback
from lib import Function
from lib.Config import Config


def group_raw_pic():
    fin = codecs.open('relation.txt', 'r', encoding='UTF-8')
    dict_group = {}
    while True:
        line = fin.readline()
        if not line:
            break
        try:
            pid, tags = line.strip('\r\n').split('\t')
            if tags not in dict_group:
                dict_group[tags] = {}
                dict_group[tags]['pic'] = ''
                dict_group[tags]['num'] = 0
            dict_group[tags]['pic'] += pid + ','
            dict_group[tags]['num'] += 1
        except:
            print traceback.format_exc()

    list_pics = []
    for tags in dict_group:
        list_pics.append([dict_group[tags]['pic'], dict_group[tags]['num']])
    list_pics.sort(key=lambda x: x[1], reverse=True)

    fout = codecs.open('group_pic.txt', 'w', encoding='UTF-8')
    group_id = 1
    for value in list_pics:
        fout.write(str(group_id)+'\t'+value[0])
        fout.write('\n')
        group_id += 1
    fout.close()
    fin.close()


def merge_pic_click():
    cf_data = Config('data.conf')
    dataset_path = cf_data.get('path', 'dataset_path')
    fin = open(dataset_path+'group_pic', 'r')
    dict_group_pic = {}
    while True:
        line = fin.readline()
        if not line:
            break
        group_id, pics = line.strip('\r\n').split('\t')
        if group_id not in dict_group_pic:
            dict_group_pic[group_id] = pics
    fin.close()

    fin = open(dataset_path+'pic_info', 'r')
    dict_raw = eval(fin.read())
    dict_output = {}
    for group_id in dict_group_pic:
        dict_output[group_id] = {}
        str_pics = dict_group_pic[group_id]
        list_pic = str_pics.strip(',').split(',')
        for pic in list_pic:
            if pic not in dict_raw:
                print 'pic not in data set: ', pic
            else:
                for day in dict_raw[pic]:
                    for page in dict_raw[pic][day]:
                        if page not in dict_output[group_id]:
                            dict_output[group_id][page] = [0, 0, day]
                            dict_output[group_id][page][0] = dict_raw[pic][day][str(page)][0]
                            dict_output[group_id][page][1] = dict_raw[pic][day][str(page)][1]
                        else:
                            dict_output[group_id][page][0] += dict_raw[pic][day][str(page)][0]
                            dict_output[group_id][page][1] += dict_raw[pic][day][str(page)][1]
                            if day not in dict_output[group_id][page][2]:
                                dict_output[group_id][page][2] += ',' + day
    fin.close()

    fout = open(dataset_path+'group_pic_position_hour', 'w')
    for group in dict_output:
        fout.write(str(group) + '\t')
        fout.write(str(dict_output[group]))
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    # group_raw_pic()
    try:
        merge_pic_click()
    except:
        print traceback.format_exc()