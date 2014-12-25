# coding: utf-8
__author__ = 'CRay'

from handlers.pb import MainHandler
from handlers.pb import ResultHandler

urls = [
    (r'/pb', MainHandler),
    (r'/result', ResultHandler),
]