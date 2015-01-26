# coding=utf-8
__author__ = 'ray'

import codecs
import traceback
from datetime import datetime, timedelta


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


def initialize_recency_range(recency_range):
    time_span = recency_range.split(',')
    list_digit_time = []
    offset = 0
    for t in time_span:
        a, b = t.split('-')
        if 'd' == b:
            offset = int(a)
        elif 'w' == b:
            offset = int(a)*7
        elif 'm' == b:
            offset = int(a)*30
        elif 'y' == b:
            offset = int(a)*365
        list_digit_time.append(offset)
    list_digit_time.sort(reverse=False)
    return list_digit_time


def get_time_index(ctime_raw, itime_raw):
    ctime = datetime.strptime(ctime_raw, '%Y-%m-%d %H:%M:%S').date()
    itime = datetime.strptime(itime_raw, '%Y-%m-%d %H:%M:%S').date()
    time_span = (itime - ctime).days
    List_recency_range_temp = List_recency_range
    List_recency_range_temp.append(time_span)
    List_recency_range_temp.sort()
    index = List_recency_range_temp.index(time_span)
    return index


def convert_data(day, unique_id):
    fin = codecs.open('/alidata1/access/dataset_'+day+'.txt', 'r', encoding='UTF-8')
    lindex_pos = -1
    lindex_pip = MAX_POS - 1
    lindex_ctime = MAX_POS + MAX_PIP - 1
    lindex_itime = MAX_POS + MAX_PIP + MAX_RECENCY_RANGE - 1
    lindex_tag = MAX_POS + MAX_PIP + MAX_RECENCY_RANGE + HOUR_RANGE - 1

    while True:
        line = fin.readline()
        if not line:
            break
        line = eval(line)
        pid = line['pid']
        pos = int(line['pos'])
        pip = int(line['pip'])
        tags = line['tags']
        ctime = line['ctime']
        itime = line['itime']
        click = int(line['click'])

        pic_location = (pos-1)*9 + pip
        unique_pic = pid + '_' + str(pic_location)

        if unique_pic not in Dict_ratio:
            Dict_ratio[unique_pic] = [0, 0]   # [show, click]
            unique_id += 1

            Dict_info[unique_pic] = {}
            Dict_info[unique_pic]['ratio'] = 0
            Dict_info[unique_pic]['pos'] = lindex_pos + pos
            Dict_info[unique_pic]['pip'] = lindex_pip + pip
            ctime_index = get_time_index(ctime, itime)
            Dict_info[unique_pic]['ctime'] = lindex_ctime + ctime_index + 1 # c_index从0开始,所以要+1
            itime_hour = datetime.strptime(itime, "%Y-%m-%d %H:%M:%S").hour
            Dict_info[unique_pic]['itime'] = lindex_itime + itime_hour + 1  # i_index从0开始,所以要+1
            Dict_info[unique_pic]['unique_id'] = unique_id  # 统计一行有多少个地方为1, 4+tag数量
            Dict_info[unique_pic]['tags'] = []
            for tag in tags:
                if tag not in Dict_tag_pos:
                    Dict_tag_pos[tag] = Dict_tag_pos['max']
                    Dict_tag_pos['max'] += 1
                tag_pos = Dict_tag_pos[tag] + lindex_tag
                Dict_info[unique_pic]['tags'].append(tag_pos)
            Dict_info[unique_pic]['tags'].sort()
        if click > 0:
            Dict_ratio[unique_pic][1] += 1
        Dict_ratio[unique_pic][0] += 1
    fin.close()
    return unique_id


def print_data(file_name):
    fout = codecs.open('/alidata1/access/result/result_'+file_name+'.txt', 'w', encoding='UTF-8')
    fout.write(str(vec_width))
    fout.write('\n')
    fout.write(str(len(Dict_ratio)))
    fout.write('\n')
    for unique_pic in Dict_info:
        try:
            click_ratio = float(Dict_ratio[unique_pic][1])/Dict_ratio[unique_pic][0]
            width = 4 + len(Dict_info[unique_pic]['tags'])

            output = str(click_ratio) + ' '
            output += str(width) + ' '
            output += str(Dict_info[unique_pic]['pos']) + ' '
            output += str(Dict_info[unique_pic]['pip']) + ' '
            output += str(Dict_info[unique_pic]['ctime']) + ' '
            output += str(Dict_info[unique_pic]['itime']) + ' '
            temp_out = ''
            for pos in Dict_info[unique_pic]['tags']:
                temp_out += str(pos) + ' '
            output += temp_out
            output += str(Dict_info[unique_pic]['unique_id'])
            fout.write(output)
            fout.write('\n')
        except:
            print Dict_info[unique_pic]
            print Dict_ratio[unique_pic]
            print traceback.format_exc()
    fout.close()


if __name__ == '__main__':
    start_time = datetime.now()
    # set threshold value
    MAX_POS = 100
    MAX_PIP = 9
    RECENCY_RANGE = '1-w,1-m,3-m,6-m,1-y'  # 不包含空格,逗号隔开类型,-隔开数字
    HOUR_RANGE = 24
    vec_width = 0

    List_recency_range = initialize_recency_range(RECENCY_RANGE)
    MAX_RECENCY_RANGE = len(List_recency_range) + 1

    Dict_ratio = {}      # for click ratio
    Dict_info = {}       # info of each line
    Dict_tag_pos = {'max': 1}    # store tag position, {'tag1': 1, 'tag2': 2 ... 'max': x}  x记录tag个数

    file_start = '2014-11-04'
    file_end = '2014-11-05'
    list_time = get_time_list(file_start, file_end)
    unique_id = 0
    for day in list_time:
        unique_id = convert_data(day, unique_id)

    vec_width = MAX_POS + MAX_PIP + MAX_RECENCY_RANGE + HOUR_RANGE + len(Dict_tag_pos) + 1
    result_name = '2014-11-04--05'
    print_data(result_name)

    end_time = datetime.now()
    print '11-04 -- 11-13  usage: ', end_time - start_time
