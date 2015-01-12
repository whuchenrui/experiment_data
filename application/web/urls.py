# coding: utf-8
__author__ = 'CRay'

from handlers.PosBaisHandler import MainHandler
from handlers.RelatePicHandler import RelatePicHandler
from handlers.TestHandler import TestHandler


urls = [
    (r'/pb', MainHandler),
    (r'/page', RelatePicHandler),
    (r'/test', TestHandler)
]