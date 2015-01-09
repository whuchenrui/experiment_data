#coding: utf-8
__author__ = 'CRay'

import ConfigParser
import json
import sys
sys.path.append(r'../../')
import traceback
import urllib
from RedisModel import RedisModel


class RelatePicModel():
    list_pic = None

    def __init__(self, date, hour, page):
        self.date = date
        self.hour = hour
        self.page = page

    def set_pic_list(self):
        redis_key = 'pp_ios7_hd_cn#hot#' + self.date + '#' + self.hour
        redis_conn = RedisModel('ranking')
        redis_conn.set_redis_key(redis_key)
        list_pic_all = redis_conn.get_pic_ranking()
        try:
            self.list_pic = list_pic_all[9*(self.page-1): 9*self.page]
            return True
        except:
            print traceback.format_exc()
            return False

    def get_pic_url(self):
        """
        :return:  返回9张图片的url地址, {key: value} key: 图片id, value: 图片url地址
        """
        dict_pic_url = {}
        for pic in self.list_pic:
            request_url = 'http://madison.appwill.com:8087/picture_by_fullname?fullname=' + pic
            appwill = urllib.urlopen(request_url)
            if 200 == appwill.getcode():
                data = appwill.read()
                json_data = json.loads(data)
                try:
                    pic_url = json_data[0]['thumb_path']
                    dict_pic_url[pic] = pic_url
                except:
                    print traceback.format_exc()
                    print '缺少thumb_path字段信息, id = '+ pic
            else:
                print '查找不到该图片, id = '+ pic
            appwill.close()
        return dict_pic_url

    def get_pic_probability(self):
        """
        :return: 返回page页上的9张图片的点击概率
        """
        cf = ConfigParser.ConfigParser()
        cf.read('../../config/data.conf')
        path = cf.get('ray', 'path')
        fin = open(path+'pic_position_hour', 'r')
        line = fin.read()
        dict_raw = eval(line)
        fin.close()

        dict_pic_probability = {}
        for pic in self.list_pic:
            try:
                probability = float(dict_raw[pic][self.page][1])/dict_raw[pic][self.page][0]
                dict_pic_probability[pic] = round(probability, 3)
            except:
                print traceback.format_exc()
        return dict_pic_probability