# coding=utf-8
__author__ = 'ray'

import ConfigParser
"""
Config() 类用于加载 conf 文件, 输入参数为conf文件名, config文件夹的绝对路径定义在构造函数里
"""


class Config():
    def __init__(self, name):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('D:\\python\\project\\highcharts\\config\\' + name)

    def get(self, section, option):
        result = self.cf.get(section, option)
        return result

    def set(self, section, option, value):
        self.cf.set(section, option, value)