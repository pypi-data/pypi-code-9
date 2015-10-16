# coding:utf-8
"""
时间:2015/10/1
说明:
"""
__author__ = 'win7-desk1'


from utils import *
from parser_collections import parse_previous, parse_special, parse_special1
from langconv import *


def to_simplified(line):
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    return line.encode('utf-8')


def pre_process(s):
    """
    预处理一下
    """
    # 先将一些无用的字符去掉
    s = s.replace(u'(', u'').replace(u')', u'')

    # 处理之前先都转换成简体
    # to_simplified 只接收str类型
    s = to_simplified(s.encode('utf-8')).decode('utf-8')
    # print u'简体:', s

    if u'民国' in s:
        return parse_special(s)

    # -------------------------------处理多少时间以前的----------------------------------
    if any(x in s for x in [u'刚刚', u'昨天', u'前天']):
        return parse_special1(s)

    if u'前' in s:
        return parse_previous(s)

    # 最后处理中文的通用模式
    # 只要有一个关键字中文存在，就用这个处理
    if any(x in s for x in u'零一二两三四五六七八九十百千万年月日时分秒早午晚号点'):
        try:
            return parse_chinese(s)
        except:
            return parse_chinese_odds(s)

    # --------------------------dateutil能处理的所有类型------------------------------------
    for restr in DUTIL_LIST:
        m = re.search(restr, s)
        if m:
            # print u'找到的正则: ', restr
            keyline = m.group(0)
            # print u'关键字: ', keyline
            # print u'日期: ', parse(keyline)
            return parse(keyline)

    # 最后试着用dateutil来处理一下
    try:
        return parse(s)
    except Exception, e:
        try:
            # 用比较全面的类来解析
            return my_custom_parse(s)
        except Exception, e1:
            print u'final error:', str(e)
    return None