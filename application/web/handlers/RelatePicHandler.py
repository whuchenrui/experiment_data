# coding=utf-8
__author__ = 'CRay'

import tornado.web
import sys
sys.path.append(r'../../')
from application.web.model.RelatePicModel import RelatePicModel
from datetime import datetime, timedelta


class RelatePicHandler(tornado.web.RequestHandler):
    def post(self):
        page = self.get_argument('page_num', default=1, strip=True)
        page = int(page)
        date = self.get_argument('date', default='2014-11-11', strip=True)
        time = self.get_argument('time', default='11:11:11', strip=True)
        time += ':00:00'
        temp_date_time = date + ' ' + time  # '2014-11-11 11:11:11'
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
            str_result = '<table border="1"><tr>'
            temp_list = []
            for pic in dict_pic_url:
                str_result += '<td class="pic"><img src="'+dict_pic_url[pic]+'"></td>'
                temp_list.append(pic)
            str_result += '</tr><tr>'
            for pic in temp_list:
                str_result += '<td class="pic_data">'+str(dict_pic_probability[pic])+'</td>'
            str_result += '</tr></table>'
            self.render('relate_pic.html', result=str_result)
        else:
            error_message = '查询第'+str(page)+'页的9张图片失败!'
            self.render('relate_pic.html', result=error_message)