# coding: utf-8
__author__ = 'CRay'

import tornado.ioloop
import sys

from settings import *

PORT = '8888'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    application.listen(PORT)
    print 'Development server is running at http://127.0.0.1:%s/' % PORT
    print 'Quit the server with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()