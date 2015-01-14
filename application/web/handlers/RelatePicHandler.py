# coding=utf-8
__author__ = 'CRay'

import tornado.web
import sys
sys.path.append(r'../../')
from application.web.model.RelatePicModel import RelatePicModel
from datetime import datetime, timedelta


class RelatePicHandler(tornado.web.RequestHandler):
    def post(self):
        page = self.get_argument('page', default=1, strip=True)
        page = int(page)
        date = self.get_argument('date', default='2014-11-11', strip=True)
        hour = self.get_argument('hour', default='11:11:11', strip=True)
        hour += ':00:00'
        temp_date_time = date + ' ' + hour  # '2014-11-11 11:11:11'
        east_time = datetime.strptime(temp_date_time, '%Y-%m-%d %H:%M:%S')
        west_time = east_time - timedelta(hours=14)
        str_west_time = west_time.strftime('%Y-%m-%d %H:%M:%S')
        date = str_west_time.split(' ')[0]
        hour = str_west_time.split(' ')[1].split(':')[0]
        relate_pic_model = RelatePicModel(date, hour, page)
        result = relate_pic_model.set_pic_list()
        if result:
            dict_pic_url = relate_pic_model.get_pic_url()
            dict_pic_probability = relate_pic_model.get_pic_probability()
            list_relate_pic = relate_pic_model.get_relate_pic_list()
            self.render('relate_pic.html', dict_url=dict_pic_url, dict_prob=dict_pic_probability
                , list_pic=list_relate_pic, page=page, date=date, hour=hour)
        else:
            error_message = '查询第 '+str(page)+' 页的图片失败!'
            self.render('error.html', result=error_message)