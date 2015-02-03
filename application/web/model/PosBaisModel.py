#coding: utf-8
__author__ = 'CRay'

import operator
import random
import sys
sys.path.append(r'../../')
from ConfigParser import ConfigParser
from lib.Mongo import Mongo


class PositionBias(object):
    def __init__(self, min_show=None, min_page=None, max_pic_num=None):
        self.min_show = min_show
        self.min_page = min_page
        self.max_pic_num = max_pic_num

    @staticmethod
    def get_file_path(name):
        cf = ConfigParser()
        cf.read('../../config/data.conf')
        file_path = cf.get('server', 'path') + name
        return file_path

    def get_specific_pic(self):
        """
        从mongodb 数据库中读取group_pic 在不同页码上的总体点击信息
        dict_output:  {group_id: {page: [show, click, time]}}
        """
        dict_output = {}
        limit_group = set()
        mongo = Mongo('kdd', 'group_pic_pb')
        group_num = mongo.collection.find().count()
        while len(limit_group) < self.max_pic_num:
            random_group = random.randint(1, group_num)
            if random_group not in dict_output:
                dict_output[random_group] = {}
                record = mongo.collection.find({'gid': random_group}, {'_id': 0})
                if record.count > 0:
                    record = record[0]['pinfo']
                    valid_point_num = 0
                    for page in record:
                        if record[page][0] >= self.min_show:
                            valid_point_num += 1
                    if valid_point_num >= self.min_page:
                        limit_group.add(random_group)
                        for page in record:
                            if page not in dict_output[random_group]:
                                if record[page][0] >= self.min_show:
                                    dict_output[random_group][page] = record[page]
                            else:
                                print 'error: ', '出现相同的page, 数据有误!'
                else:
                    print str(random_group), ' 不存在 '
        mongo.close()
        list_data = PositionBias.print_pb(dict_output)
        return list_data

    @staticmethod
    def print_pb(result):
        list_output = []
        for picture in result:
            dict_per_pic = {}
            temp = result[picture]
            sorted_tuple = sorted(temp.items(), key=lambda d: d[0], reverse=True)
            list_temp = []
            for i in range(0, len(sorted_tuple)):
                pic_temp = {}
                page = sorted_tuple[i][0]
                probability = round(float(sorted_tuple[i][1][1])/sorted_tuple[i][1][0], 3)
                pic_temp["x"] = page
                pic_temp["y"] = probability
                pic_temp["z"] = sorted_tuple[i][1][2]
                list_temp.append(pic_temp)
            list_temp_sorted = sorted(list_temp, key=operator.itemgetter('x'))
            dict_per_pic["name"] = int(picture)
            dict_per_pic["data"] = list_temp_sorted
            list_output.append(dict_per_pic)
        return list_output

    @staticmethod
    def merge_pics_into_one_line(min_show, min_page):
        file_path = PositionBias.get_file_path('group_pic_position_hour')
        dict_output = {}
        fin = open(file_path, 'r')
        dict_raw = eval(fin.readline())
        for picture in dict_raw:
            count = 0
            temp = {}
            for page in dict_raw[picture]:
                if dict_raw[picture][page][0] > min_show:
                    count += 1
                    temp[page] = dict_raw[picture][page]
            if count < min_page:
                continue
            for page in temp:
                if page not in dict_output:
                    dict_output[page] = [0, 0]
                dict_output[page][0] += temp[page][0]
                dict_output[page][1] += temp[page][1]
        fin.close()
        list_output = []
        for i in range(1, 100):
            if i not in dict_output:
                continue
            temp = float(dict_output[i][1])/dict_output[i][0]
            list_output.append([i, round(temp, 3)])
        return list_output

if __name__ == '__main__':
    PositionBias.get_pb_hour()
