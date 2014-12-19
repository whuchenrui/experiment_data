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
    :return: dict_bias  {pic1: {key: [a, b]}}  key: 图片出现的位置， a图片呈现次数， b图片被点击次数
    :return:  page_min  pic至少出现的次数
    """
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')

    #TODO： 此处要修改， else 的默认为 result
    if _type == 'save':
        name = 'pic_raw'
        name2 = 'result_raw'
    else:
        name = 'pic'
        name2 = 'result'
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


def find_pic(min_pos_num, min_click_num, variance):
    flag = False
    key_pic = None
    list_key_pic = []
    set_pic = set()
    dict_bias = {}     # {pic : [[1, 4, 9], [0.3, 0.25, 0.11]], pic2: [[], []]}

    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    fin = codecs.open(source_path+'pic_position', 'r', encoding='UTF-8')
    dict_raw = eval(fin.readline())
    fin.close()

    # 去除每张图片呈现非常少的二元组, 构造存放图片出现位置和点击概率的字典 pic: [[], []]
    for pic in dict_raw:
        list_pic_page_prob = []
        for page in dict_raw[pic]:
            if dict_raw[pic][page][0] > min_click_num:
                probability_temp = float(dict_raw[pic][page][1])/dict_raw[pic][page][0]
                temp_prob = [page, round(probability_temp, 3)]
                list_pic_page_prob.append(temp_prob)
        if len(list_pic_page_prob) > min_pos_num:
            list_pic_page_prob.sort(key=lambda x: x[0])
            sorted_page = []
            sorted_prob = []
            for i in range(0, len(list_pic_page_prob)):
                sorted_page.append(list_pic_page_prob[i][0])
                sorted_prob.append(list_pic_page_prob[i][1])
            sorted_page_prob = [sorted_page, sorted_prob]
            dict_bias[pic] = sorted_page_prob

    while not flag:
        key_pic = choice(dict_bias.keys())
        if min_pos_num < len(dict_bias[key_pic][0]):
            flag = True
    len_key_pic = len(dict_bias[key_pic][0])
    list_key_pic = dict_bias[key_pic]
    for pic in dict_bias:
        if len(dict_bias[pic][0]) < min_pos_num:
            continue
        flag = True
        temp_prob = dict_bias[pic][1]
        for i in range(0, len(temp_prob)-1):
            if temp_prob[i+1] > temp_prob[i]:
                flag = False
                break
        if not flag:
            continue
        set_pic.add(pic)
        # flag = False  # 记录A是否一直在B上方
        # is_positive = False  # 记录AB那一条线在上方
        # list_temp_pic = dict_bias[pic]
        # step = 4
        # len_temp_pic = len(dict_bias[pic][0])
        # if len_key_pic < len_temp_pic:
        #     small_len = len_key_pic
        # else:
        #     small_len = len_temp_pic
        # for i in range(0, (small_len+step-1)/step):   # 此处的step为步幅，每次比对step个单位内AB是否满足A最大值小于B最小值
        #     key_pos = 0
        #     temp_pos = i * step + step
        #     for j in range(i*step, i*step+step):
        #         if j in list_key_pic[0]:   # 找到step范围内key_pic的最小值
        #             key_pos = j
        #         if j in list_temp_pic[0]:     # 找到step范围内temp_pic的最大值
        #             if temp_pos > j:
        #                 temp_pos = j
        #     if

    print set_pic
    fout = codecs.open(chart_data+'pic_position_bias.log', 'w', encoding='UTF-8')
    fout.write('line: \n')
    # for pic in set_pic:
    #     output = []
    #     for item in dict_bias[pic]:
    #         output.append([item, dict_bias[pic][item][0]])
    #         output.sort(key=lambda x: x[0])
    #     fout.write("{ name: '" + pic + "', type: 'column', yAxis: 1,  data: ")
    #     fout.write(str(output))
    #     fout.write('}, \n')
    for pic in set_pic:
        output = []
        for i in range(0, len(dict_bias[pic][0])):
            output.append([dict_bias[pic][0][i], dict_bias[pic][1][i]])
        fout.write("{ name: '" + pic + "', data: ")
        fout.write(str(output))
        fout.write('}, \n')
    fout.close()


if __name__ == '__main__':
    get_pic_click('view', 30, 3)
