__author__ = 'CRay'

import tornado.web
import sys
sys.path.append(r'../../')


class TestHandler(tornado.web.RequestHandler):
    def post(self):
        page = self.get_argument('page', default=1, strip=True)
        page = int(page)
        date = self.get_argument('date', default='2014-11-11', strip=True)
        hour = self.get_argument('hour', default='11:11:11', strip=True)
        print page, ' ', date, ' ', hour
        list_pic = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        dict_pic = {'1': 'http://lh5.ggpht.com/-OXgHwJgiLkc/U-iPbPjg5KI/AAAAAAAA1V4/95DBUmwlrEI/s320/1.jpg',
                    '2': 'http://lh5.ggpht.com/-O9pLQHxB4JU/U4-SPYicQTI/AAAAAAABBXI/zGt7pZwVoxs/s320/1.jpg',
                    '3': 'http://lh3.ggpht.com/-E05I_gowMow/Ur6cdnsWeyI/AAAAAAAAeoI/9USs0SWut7Y/s320/1.jpg',
                    '4': 'http://lh3.ggpht.com/-u-dSiA7XwVA/VAi1xnNoKNI/AAAAAAABG3E/lzSLNKBB1_Q/s320/1.jpg',
                    '5': 'http://lh5.ggpht.com/-OXgHwJgiLkc/U-iPbPjg5KI/AAAAAAAA1V4/95DBUmwlrEI/s320/1.jpg',
                    '6': 'http://lh5.ggpht.com/-O9pLQHxB4JU/U4-SPYicQTI/AAAAAAABBXI/zGt7pZwVoxs/s320/1.jpg',
                    '7': 'http://lh3.ggpht.com/-E05I_gowMow/Ur6cdnsWeyI/AAAAAAAAeoI/9USs0SWut7Y/s320/1.jpg',
                    '8': 'http://lh3.ggpht.com/-u-dSiA7XwVA/VAi1xnNoKNI/AAAAAAABG3E/lzSLNKBB1_Q/s320/1.jpg',
                    '9': 'http://lh3.ggpht.com/-u-dSiA7XwVA/VAi1xnNoKNI/AAAAAAABG3E/lzSLNKBB1_Q/s320/1.jpg'}
        print list_pic, dict_pic
        self.flush()
        self.render('test.html', list_pic=list_pic, dict_pic=dict_pic)