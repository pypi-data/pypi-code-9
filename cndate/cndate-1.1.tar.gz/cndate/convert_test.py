# coding:utf-8
"""
时间:2015/9/28
说明:
https://github.com/skydark/nstools/blob/master/zhtools/zh_wiki.py

"""
__author__ = 'win7-desk1'

from langconv import *


def cvt(line):
    print '-', line
    # 转换繁体到简体
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    print '--', line

    # 转换简体到繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')

    print '--', line


def to_simplified(line):
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    return line.encode('utf-8')


def to_traditional(line):
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    return line.encode('utf-8')


if __name__ == '__main__':
    # line = '中文簡繁轉換開源項目，支持詞彙級別的轉換、異體字轉換和地區習慣用詞轉換（中國大陸、臺灣、香港）'
    # cvt(line)
    word = u'2小时前'.encode('utf-8')
    print to_simplified(word)
    print to_traditional(word)
    pass
