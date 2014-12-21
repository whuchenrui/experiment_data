# coding: utf-8
__author__ = 'CRay'

import tornado.web
from application.web.model.pic_posi_bias import PositionBias
from application.pic_click.picture_position_bias import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ResultHandler(tornado.web.RequestHandler):
    def post(self):
        min_show = self.get_argument('min_show', 500, strip=True)
        min_show = int(min_show)
        min_page = self.get_argument('min_page', 5, strip=True)
        min_page = int(min_page)
        entity = PositionBias.get_pic_pb(min_show, min_page)
        self.render('position_bias.html', entity=entity)
