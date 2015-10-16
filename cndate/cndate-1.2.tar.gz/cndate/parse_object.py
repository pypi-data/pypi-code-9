# coding:utf-8
"""
时间:2015/10/7
说明: 自定义解析
"""
__author__ = 'win7-desk1'
from dateutil.parser import parse


class ParseObject(object):

    def __init__(self, s):
        self.s = s.lower().strip()
        self.d = None  # 用于表示最终解析出的日期
        self.parse()

    def parse(self):
        # 开始解析
        pass



    def get_res(self):
        print self.s
        return None



if __name__ == '__main__':
    s = u' Mon Oct  5 15:03:30 2015'
    po = ParseObject(s)
    po.get_res()