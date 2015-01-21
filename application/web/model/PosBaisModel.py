#coding: utf-8
__author__ = 'CRay'

import operator
import sys
sys.path.append(r'../../')
from random import choice
from ConfigParser import ConfigParser


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
        file_path = PositionBias.get_file_path('group_pic_position_hour')
        dict_output = {}
        limit_pic = set()
        fin = open(file_path, 'r')
        dict_raw = eval(fin.readline())
        while len(limit_pic) < self.max_pic_num:
            random_pic = choice(dict_raw.keys())
            count = 0
            temp = {}
            for page in dict_raw[random_pic]:
                if dict_raw[random_pic][page][0] > self.min_show:
                    count += 1
                    temp[page] = dict_raw[random_pic][page]
            if count < self.min_page:
                continue
            dict_output[random_pic] = temp
            limit_pic.add(random_pic)
        fin.close()
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
