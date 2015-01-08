# coding: utf-8
__author__ = 'CRay'

from handlers.PosBaisHandler import MainHandler
from handlers.PosBaisHandler import PicHourHandler


urls = [
    (r'/pb', MainHandler),
    (r'/hour', PicHourHandler),
    (r'/page', PicHourHandler),
]