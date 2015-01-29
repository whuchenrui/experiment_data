# coding=utf-8
__author__ = 'CRay'
from lib.Config import Config
"""
设置过滤条件, 无效序列返回False
过滤4中情况
1: 长度过长, 删去 > max_request_num
2: 序列全为0
3: 序列1占比过多, 删去 > max_click_percent
4: 序列连续1过长, 删去 > max_sub_seq_length
"""


class FilterRule():
    def __init__(self, name, act_type):
        cf = Config(name)
        self.max_request_num = int(cf.get('filter_value', 'max_request_num'))
        self.max_sub_seq_length = int(cf.get('filter_value', 'max_sub_seq_length'))
        self.max_click_percent = float(cf.get('filter_value', 'max_click_percent'))
        temp = cf.get('filter_value', 'act_time')
        self.act_time = temp.split(',')
        self.act_type = act_type

    def check_each_seq(self, result):
        length = len(result)
        request = length/36
        if request > self.max_request_num:
            return False
        click_num = FilterRule.get_click_cnt(result, self.act_type)
        if click_num == 0:
            return False
        percent = int(float(click_num)/length*100)
        if percent > self.max_click_percent:
            return False
        max_len = FilterRule.get_sub_seq_cnt(result, self.act_type, length)
        if max_len > self.max_sub_seq_length:
            return False
        return True

    @staticmethod
    def get_click_cnt(line, value):
        cnt = 0
        for item in line:
            if item >= value:
                cnt += 1
        return cnt

    @staticmethod
    def get_sub_seq_cnt(line, value, length):
        c_len = 0               # 当前最长1序列长度
        max_len = 0             # 最大1序列长度
        for i in range(0, length):
            if line[i] >= value:
                if c_len > 0:
                    c_len += 1
                else:
                    c_len = 1
            else:
                if c_len > max_len:
                    max_len = c_len
                c_len = 0
        if c_len > max_len:    # 处理最后一个数字为1的情况
            max_len = c_len
        return max_len
