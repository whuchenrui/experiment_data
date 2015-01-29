# coding=utf-8
__author__ = 'CRay'
from datetime import datetime, timedelta


def get_time_list(time_st, time_end):
    time_st = datetime.strptime(time_st, '%Y-%m-%d')
    time_end = datetime.strptime(time_end, '%Y-%m-%d')
    time3 = time_st
    time_len = (time_end - time_st).days + 1
    num = 0
    list_time = list()
    while num < time_len:
        t3 = time3.strftime('%Y-%m-%d')
        time3 += timedelta(days=1)
        list_time.append(t3)
        num += 1
    return list_time