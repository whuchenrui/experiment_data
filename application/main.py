# coding=utf-8
__author__ = 'CRay'
from application.dataset.link_file import *
from application.dataset.link_file_hour_pb import *
from application.dataset.filter_data import *
from application.pic_click.average_click_user_distribution import *
from application.pic_click.picture_quality import *
from application.pic_click.page_positon_bais import *
from application.turn.general_turn import *
from application.turn.turn_probability import *


def main_link_files():
    """ 整合每小时产生的序列，合并为一个文件，未过滤。返回序列总长度，
    并找出大于K次请求后，只剩5%的用户时候的请求数值，方便下一轮过滤 """
    folder_st = '2014-11-04'
    folder_end = '2014-11-24'
    line_cnt, filter_req = link(folder_st, folder_end)
    print '产生记录： ' + str(line_cnt) + '条'
    print '98% is: ' + str(filter_req)
    return filter_req


def main_filter_data(_filter_request, _type):
    """ 扫描结果集合，获得1的子序列使用情况，根据图表，设置过滤条件. 3个过滤条件，均过滤5%。总体过滤<30% """
    get_view_ratio()
    max_len, max_percent = get_sub_seq()
    # view的时候需要filter， 但是save时候，不需要执行该函数
    print 'sub_seq cal finish:', max_len, max_percent
    if _type == 'view':
        count = filter_data(max_len, max_percent)
        print '删去1子序列后剩余： ' + str(count)
        count = remove_too_long_seq(_filter_request)
        print '删去过长序列后剩余： ' + str(count)


def main_pic_click(_filter_req, _type):
    """ 画平均点击图和点图 """
    distribution(_type)                       # 用户序列分布图
    print 'User distribution finish !'
    average_click(_filter_req, _type)         # 平均点击图
    print 'Average click finish ! '
    quality(_type)                            # 点图，证明图片质量差别
    print 'Picture quality finish !'
    position_bias(_filter_req, _type)         # page的postion图
    print 'Page position bias finish !'


def main_turn_probability(_action):
    # general_turn(_action)
    print 'General turn finish !'
    turn_probability(_action, 2, 15, 20, 2, 0)
    print 'Turn probability with last 8 pages finish !'


if __name__ == '__main__':
    # TODO:修改view的时候，一定要顺带修改data.conf 中的type为相应值！！！！
    act_type = 'view'
    # filter_request = main_link_files()
    # main_filter_data(27, act_type)
    # main_pic_click(27, act_type)
    # main_turn_probability(act_type)
    link_hour('2014-11-03', '2014-11-24', 27, 5)  # 开始日期, 结束日期, 统计27*4页内的信息, 至少出现的页码数
