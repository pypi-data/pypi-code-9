# coding:utf-8
from process import pre_process


def cnparse(s):
    return pre_process(s)


if __name__ == '__main__':
    print cnparse(u'2015-1-21 11:52 PM')