# coding=utf-8
__author__ = 'ray'

import codecs
import os
from ConfigParser import ConfigParser
from random import choice


def get_pic_click(_type, request_num, page_min):
    """
    :param _type:  save  or  view
    :param filter_cnt:   seq最大长度，超过的部分不计算。
    :return: dict_bias  {pic1: {key: [a, b]}}  key: 图片出现的位置， a 图片呈现次数， b图片被点击次数
    :return:  page_min  pic至少出现的次数
    """
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    action = int(cf.get('type', 'type'))

    #TODO： 此处要修改， else 的默认为 result
    if _type == 'save':
        name = 'pic_raw'
        name2 = 'result_raw'
    else:
        name = 'pic_raw'
        name2 = 'result_raw'
    dict_bias = {}
    filter_cnt = request_num * 36
    fin_pic = codecs.open(source_path+name, 'r', encoding='UTF-8')
    fin_result = codecs.open(source_path+name2, 'r', encoding='UTF-8')
    while True:
        line_pic = fin_pic.readline()
        line_result = fin_result.readline()
        if not line_pic:
            break
        pic = line_pic.strip('\n').split(' ')
        result = line_result.strip('\n').split(' ')
        length = len(result)
        if length > filter_cnt:
            length = filter_cnt
        for index, item in enumerate(result):
            result[index] = int(item)
        for i in range(0, length):
            page = i/9 + 1
            picture = pic[i]
            if picture not in dict_bias:
                dict_bias[picture] = {}
            if page not in dict_bias[picture]:
                dict_bias[picture][page] = [0, 0]
            if result[i] > 0:
                dict_bias[picture][page][1] += 1
            dict_bias[picture][page][0] += 1
    fin_pic.close()
    fin_result.close()

    dict_output = {}
    for item in dict_bias:
        if len(dict_bias[item]) > page_min:
            dict_output[item] = dict_bias[item]
    fout = codecs.open(source_path+'pic_position', 'w', encoding='UTF-8')
    str_dict = str(dict_output)
    fout.write(str_dict)
    fout.close()


def find_pic(max_pos_num, min_pos_num, min_click_num, variance):
    flag = False
    key_pic = None
    list_key_pic = []
    set_pic = set()
    dict_bias = {}

    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    fin = codecs.open(source_path+'pic_position', 'r', encoding='UTF-8')
    dict_raw = eval(fin.readline())
    fin.close()

    # 去除每张图片呈现非常少的二元组
    for pic in dict_raw:
        dict_temp = {}
        for page in dict_raw[pic]:
            if dict_raw[pic][page][0] > min_click_num:
                dict_temp[page] = dict_raw[pic][page]
        if len(dict_temp) > min_pos_num:
            dict_bias[pic] = dict_temp

    while not flag:
        key_pic = choice(dict_bias.keys())
        if min_pos_num < len(dict_bias[key_pic]) < max_pos_num:
            flag = True
    for i in dict_bias[key_pic]:
        list_key_pic.append(i)
    list_key_pic.sort()
    print key_pic, list_key_pic
    len_key_pic = len(dict_bias[key_pic])
    for i in dict_bias:
        if len(dict_bias[i]) < min_pos_num:
            continue
        elif len(dict_bias[i]) > max_pos_num:
            continue
        else:
            total = 0
            list_temp_pic = []
            for j in dict_bias[i]:
                list_temp_pic.append(j)
            list_temp_pic.sort()
            len_temp = len(list_temp_pic)
            if len_temp < len_key_pic:
                small = len_temp
                small_list = list_temp_pic
                large = len_key_pic
                large_list = list_key_pic
            else:
                small = len_key_pic
                small_list = list_key_pic
                large = len_temp
                large_list = list_temp_pic
            for j in range(0, small):
                min_variance = abs(large_list[j] - small_list[j])
                k = j
                while True:
                    k += 1
                    if k >= large:
                        total += min_variance
                        break
                    temp = abs(large_list[k] - small_list[j])
                    if temp >= min_variance:
                        total += min_variance
                        break
                    else:
                        min_variance = temp
        if total < variance:
            set_pic.add(i)
    print set_pic
    fout = codecs.open(chart_data+'pic_position_bias.log', 'w', encoding='UTF-8')
    fout.write('column: \n')
    for pic in set_pic:
        output = []
        for item in dict_bias[pic]:
            output.append([item, dict_bias[pic][item][0]])
            output.sort(key=lambda x: x[0])
        fout.write("{ name: '" + pic + "', type: 'column', yAxis: 1,  data: ")
        fout.write(str(output))
        fout.write('}, \n')
    fout.write('\n \n line: \n')
    for pic in set_pic:
        output = []
        for item in dict_bias[pic]:
            probability = float(dict_bias[pic][item][1])/dict_bias[pic][item][0]
            output.append([item, round(probability, 3)])
            output.sort(key=lambda x: x[0])
        fout.write("{ name: '" + pic + "', data: ")
        fout.write(str(output))
        fout.write('}, \n')
    fout.close()


if __name__ == '__main__':
    get_pic_click('view', 30, 3)
