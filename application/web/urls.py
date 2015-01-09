# coding: utf-8
__author__ = 'CRay'

from handlers.PosBaisHandler import MainHandler
from handlers.PosBaisHandler import PicHourHandler
from handlers.RelatePicHandler import RelatePicHandler


urls = [
    (r'/pb', MainHandler),
    (r'/hour', PicHourHandler),
    (r'/page', RelatePicHandler),
]