# coding=utf-8
__author__ = 'CRay'

import codecs
from ConfigParser import ConfigParser

# 1：统计最长为1的子序列的情况，并计算所占百分比
# 2：设置过滤条件，过滤掉噪音数据


def get_sub_seq_cnt(line, action, length):
    c_len = 0               # 当前最长1序列长度
    max_len = 0             # 最大1序列长度
    for i in range(0, length):
        if line[i] >= action:
            if c_len > 0:
                c_len += 1
            else:
                c_len = 1
        else:
            if c_len > max_len:
                max_len = c_len
            c_len = 0
    if c_len > max_len:   # 处理最后一个数字为1的情况
        max_len = c_len
    return max_len


def get_click_cnt(line, action):
    cnt = 0
    for item in line:
        if item >= action:
            cnt += 1
    return cnt


def get_view_ratio():
    """
    dict_view = {}    记录用户点击的图片，占整个序列的比例
    """
    dict_view = {}
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    action = int(cf.get('type', 'type'))

    fin = codecs.open(source_path+'result_raw', 'r', encoding='utf-8')
    total = 0
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.strip('\n').split(' ')
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        click_cnt = get_click_cnt(list_res, action)
        length = len(list_res)
        per_cent = int(float(click_cnt)/length*100)       # 不是四舍五入，效果为向下取整，数值表示百分比
        if per_cent not in dict_view:
            dict_view[per_cent] = 0
        dict_view[per_cent] += 1
        total += 1
    fin.close()

    a = []  # 柱状图，每个横坐标占总体的百分比
    b = []  # 折线图，小于等于当前比例的占总体的百分比
    temp = 0
    for i in range(0, 50):
        if i not in dict_view:
            a.append([0, 0])
        else:
            percent = round(float(dict_view[i])/total, 3)
            a.append([i, percent])
            temp += percent
        temp_output = round(temp, 3)
        b.append([i, temp_output])
    fout = open(chart_data+'0-data-view.result', 'w')
    fout.write('column:\n')
    fout.write(str(a))
    fout.write('\n')
    fout.write('line:\n')
    fout.write(str(b))
    fout.write('\n')
    fout.close()


def get_sub_seq():
    """
    get_sub_seq_cnt   获得最长1的子序列的长度
    dict_seq = {}     记录最长1子串的情况 {1: 55, 2: 17}  1个数： seq条数
    dict_seq_ratio = {}  记录最长1子串占当前seq的比例 {1: 0.25} 长1串占序列的比例，该比例的seq占总seq比例
    """
    dict_seq = {}
    dict_seq_ratio = {}
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    chart_data = cf.get('dataset', 'chart')
    action = int(cf.get('type', 'type'))
    sub_seq_length = float(cf.get('percent', 'sub_seq_length'))
    sub_seq_percent = float(cf.get('percent', 'sub_seq_percent'))

    fin = codecs.open(source_path+'result_raw', 'r', encoding='utf-8')
    total = 0
    while True:
        line = fin.readline()
        if not line:
            break
        list_res = line.strip('\n').split(' ')
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        length = len(list_res)
        max_len = get_sub_seq_cnt(list_res, action, length)
        if max_len not in dict_seq:
            dict_seq[max_len] = 0
        dict_seq[max_len] += 1

        per_cent = int(float(max_len)/length*100)
        if per_cent not in dict_seq_ratio:
            dict_seq_ratio[per_cent] = 0
        dict_seq_ratio[per_cent] += 1

        total += 1
    fin.close()

    a = []   # 当前横坐标对应的seq占所有seq的比例
    b = []   # 小于等于当前坐标对应的seq占所有的比例
    temp = 0
    rule_length = 0  # 子序列1的长度大于rule_length会被删除
    for i in range(0, 50):
        if i not in dict_seq:
            a.append([0, 0])
        else:
            ratio = round(float(dict_seq[i])/total, 3)
            a.append([i, ratio])
            temp += ratio
        temp_output = round(temp, 3)
        b.append([i, temp_output])
        if temp < sub_seq_length:
            rule_length = i
    fout = open(chart_data+'0-data-sub-seq.result', 'w')
    fout.write('Data about length of seq 1 (picture 1):\n')
    fout.write('ratio of per length:\n')
    fout.write(str(a))
    fout.write('\n')
    fout.write('sum of ratio no more than this length:\n')
    fout.write(str(b))
    fout.write('\n')

    a = []
    b = []
    rule_percent = 0    # 1占序列比大于rule_percent会被删除
    temp = 0
    for i in range(0, 50):
        if i not in dict_seq_ratio:
            a.append([0, 0])
        else:
            ratio = round(float(dict_seq_ratio[i])/total, 3)
            a.append([i, ratio])
            temp += ratio
        temp_output = round(temp, 3)
        b.append([i, temp_output])
        if temp < sub_seq_percent:
            rule_percent = i
    fout.write('Data about ratio of sub seq 1 (picture 2):\n')
    fout.write('ratio of this percentage:\n')
    fout.write(str(a))
    fout.write('\n')
    fout.write('sum of ratio no more than this percentage:\n')
    fout.write(str(b))
    fout.write('\n')
    fout.close()

    return rule_length, rule_percent

#################filter data#################


def filter_rule(line, action, max_length, percent):
    length = len(line)
    max_len = get_sub_seq_cnt(line, action, length)
    # click_num = get_click_cnt(line, action)
    if max_len > max_length:
        return False
    elif int((float(max_len)/length)*100) > percent:
        return False
    # TODO: 暂时注释 click/view<0.01 过滤条件
    # elif (float(click_num)/length) < 0.01:
    #     return False
    return True


def filter_data(max_len, max_percent):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    action = int(cf.get('type', 'type'))

    fin_pic = open(source_path+'pic_raw', 'r')
    fin_result = open(source_path+'result_raw', 'r')

    fout_pic = open(source_path+'pic_temp', 'w')
    fout_result = open(source_path+'result_temp', 'w')

    # fout_filter_pic = codecs.open(source_path+'pic_filter', 'w', encoding='utf-8')
    # fout_filter_result = codecs.open(source_path+'result_filter', 'w', encoding='utf-8')

    count = 0
    while True:
        line_pic = fin_pic.readline()
        line_result = fin_result.readline()
        if not line_result:
            break
        list_res = line_result.strip('\n').split(' ')
        for index, item in enumerate(list_res):
            list_res[index] = int(item)
        flag = filter_rule(list_res, action, max_len, max_percent)
        if flag:
            count += 1
            fout_pic.write(line_pic)
            fout_result.write(line_result)
    fin_pic.close()
    fin_result.close()
    fout_pic.close()
    fout_result.close()
    return count


def remove_too_long_seq(req_num):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')

    fin_pic = open(source_path+'pic_temp', 'r')
    fin_result = open(source_path+'result_temp', 'r')

    fout_pic = open(source_path+'pic', 'w')
    fout_result = open(source_path+'result', 'w')

    count = 0
    while True:
        line_pic = fin_pic.readline()
        line_result = fin_result.readline()
        if not line_result:
            break
        list_res = line_result.strip('\n').split(' ')
        if len(list_res)/36 > req_num:
            continue
        count += 1
        fout_pic.write(line_pic)
        fout_result.write(line_result)
    fin_pic.close()
    fin_result.close()
    fout_pic.close()
    fout_result.close()
    return count