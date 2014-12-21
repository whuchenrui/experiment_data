__author__ = 'CRay'

from urls import *

import tornado.web
import os
SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
)

application = tornado.web.Application(
    handlers= urls,
    **SETTINGS
)