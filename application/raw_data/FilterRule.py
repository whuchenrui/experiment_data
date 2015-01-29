# coding=utf-8
__author__ = 'CRay'
from lib.Config import Config
"""
设置过滤条件, 无效序列返回False
"""


class FilterRule():
    def __init__(self):
        pass

    @staticmethod
    def check_each_seq(result, act_time):
