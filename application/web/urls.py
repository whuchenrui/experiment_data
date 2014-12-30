# coding: utf-8
__author__ = 'CRay'

from handlers.pb import MainHandler
from handlers.pb import PicHourHandler

urls = [
    (r'/pb', MainHandler),
    (r'/hour', PicHourHandler),
]