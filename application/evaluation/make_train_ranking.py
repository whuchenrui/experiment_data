# coding=utf-8
__author__ = 'CRay'

from lib.Config import Config
from lib.Mongo import Mongo


def train_data_baseline_all(behavior, dict_time):
    db_name = 'pic_info_' + behavior
    mongo = Mongo('kdd', db_name)
    list_pic_click = []
    list_pic_probability = []
    record = mongo.collection.find({}, {'_id': 0})
    if record.count() > 0:
        for r in record:
            pic = r['pid']
            click_num = 0
            show_num = 0
            for day in dict_time:
                for hour in dict_time[day]:
                    full_time = day + ':' + hour
                    if full_time in r:
                        click_num += r[full_time][1]
                        show_num += r[full_time][0]
            if show_num > 0:
                prob = float(click_num)/show_num
                list_pic_probability.append([round(prob, 4), pic])
            else:
                list_pic_probability.append([0, pic])
            list_pic_click.append([click_num, pic])
    else:
        print '记录数为0'
    mongo.close()
    list_pic_click.sort(key=lambda x: x[0], reverse=True)
    list_pic_probability.sort(key=lambda x: x[0], reverse=True)
    list_out_click = []
    list_out_prob = []
    for item in list_pic_click:
        list_out_click.append(item[1])
    for item in list_pic_probability:
        list_out_prob.append(item[1])
    print 'baseline 图片总数: ', len(list_out_click), len(list_pic_probability)
    return list_out_click, list_out_prob


def train_data_position_bias(data_name):
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fin = open(path+data_name+'.txt', 'r')
    line = fin.readline()
    list_pic = line.strip('\r\n').split(',')
    fin.close()
    print 'pb, 图片总数: ', len(list_pic)
    return list_pic


def train_data_full_model(data_name):
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fin = open(path+data_name+'.txt', 'r')
    line = fin.readline()
    list_pic = line.strip('\r\n').split(',')
    fin.close()
    print 'full model, 图片总数: ', len(list_pic)
    # data_name = data_name.split('data3')[1]
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
        print 'Union size: ', len(new_rank_click)
        return new_rank_click, new_rank_prob, new_rank_pb, new_rank_full
    else:
        print '集合不相等, ', str(len(new_rank_click)), str(len(new_rank_prob)), \
            str(len(new_rank_pb)), str(len(new_rank_full))
        return new_rank_click, new_rank_prob, new_rank_pb, new_rank_full


if __name__ == '__main__':
    # St_time = '2014-11-04'
    # End_time = '2014-11-06'
    # data3_full_raw = data_full_model(4000)
    # data2_pb, data3_full, pic_num = data_position_bias(data3_full_raw)
    # Pic_group_baseline = data_baseline(St_time, End_time, data2_pb)
    click, prob = train_data_baseline_all('2014-11-11', '2014-11-11')