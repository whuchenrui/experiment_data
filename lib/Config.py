# coding=utf-8
__author__ = 'ray'

import ConfigParser
"""
Config() 类用于加载 conf 文件, 输入参数为conf文件名, config文件夹的绝对路径定义在构造函数里
"""


class Config():
    def __init__(self, name):
        self.cf = ConfigParser.ConfigParser()
        self.file_name = 'D:\\python\\project\\highcharts\\config\\' + name
        self.cf.read(self.file_name)

    def get(self, section, option):
        result = self.cf.get(section, option)
        return result

    def set(self, section, option, value):
        self.cf.set(section, option, value)

    def write(self):
        self.cf.write(open(self.file_name, 'w'))