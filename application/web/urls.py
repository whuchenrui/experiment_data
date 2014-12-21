# coding: utf-8
__author__ = 'CRay'

from handlers.index import MainHandler
from handlers.index import ResultHandler

urls = [
    (r'/pb', MainHandler),
    (r'/result', ResultHandler),
]