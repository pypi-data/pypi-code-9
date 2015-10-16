# coding:utf-8
from process import pre_process


def cparse(s):
    return pre_process(s)


if __name__ == '__main__':
    print cparse(u'2015-1-21 11:52 PM')