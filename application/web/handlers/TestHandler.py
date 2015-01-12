__author__ = 'CRay'

import tornado.web
import sys
sys.path.append(r'../../')


class TestHandler(tornado.web.RequestHandler):
    def post(self):
        list_pic = ['1', '2', '3', '4']
        dict_pic = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
        self.render('test.html', list_pic=list_pic, dict_pic=dict_pic)