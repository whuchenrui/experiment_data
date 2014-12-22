#coding:utf-8
__author__ = 'CRay'

from ConfigParser import ConfigParser
import codecs
import operator


class PositionBias(object):
    def __init__(self, min_show, min_page):
        self.min_show = min_show
        self.min_page = min_page
        self.data = PositionBias.filter_data(self.min_show, self.min_page)

    @staticmethod
    def filter_data(min_show, min_page):
        dict_output = {}
        fin = codecs.open('D:/python/project/highcharts/data/dataset/pic_position_hour', 'r', encoding='utf-8')
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
            dict_output[picture] = temp
        fin.close()
        list_data = PositionBias.print_data(dict_output)
        return list_data

    @staticmethod
    def print_data(result):
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
    def get_pic_pb(min_show, min_page):
        return PositionBias(min_show, min_page)