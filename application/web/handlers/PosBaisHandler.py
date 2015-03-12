# coding: utf-8
__author__ = 'CRay'

import tornado.web
import sys
sys.path.append(r'../../')
from tornado.escape import json_encode
from application.web.model.PosBaisModel import PositionBias


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('position_bias.html')

    def post(self):
        min_show = self.get_argument('min_show', default=500, strip=True)
        if not min_show:
            min_show = 500
        else:
            min_show = int(min_show)
        min_page = self.get_argument('min_page', default=8, strip=True)
        if not min_page:
            min_page = 8
        else:
            min_page = int(min_page)
        max_pic_num = self.get_argument('max_pic_num', default=10, strip=True)
        if not max_pic_num:
            max_pic_num = 10
        else:
            max_pic_num = int(max_pic_num)
        function_type = int(self.get_argument('total', default=0, strip=True))
        entity = PositionBias(min_show, min_page, max_pic_num)
        if function_type == 0:
            # function_type 对应position_bias.html  0表示click/show按钮  1表示show/save按钮
            data = entity.get_specific_pic_click_show()
        else:
            data = entity.get_specific_pic_save_click()
        self.write(json_encode(data))
