# coding:utf-8
"""
时间:2015/10/1
说明:
"""
from datetime import timedelta
from datetime import datetime as dt
from utils import *
from datetime import datetime


def parse_special(s):
    try:
        # 民国
        # m = re.match(ur"(\d+)\.(\d+)", "24.1632")  # ('24', '1632')
        m = re.search(ur"(民国)(\d+)(年)", s)
        if m.groups() and len(m.groups()) >= 2:
            # print u'找到年份: ', m.group(2)
            return datetime(year=1911+int(m.group(2)), month=1, day=1)
    except Exception, e:
        print 'error', str(e)

    return None


def parse_special1(s):
    # [u'刚刚', u'昨天', u'前天']
    if u'刚刚' in s:
        # 一分钟前
        return dt.now() - timedelta(minutes=1)

    if u'昨天' in s:
        return dt.now() - timedelta(days=1)

    if u'前天' in s:
        return dt.now() - timedelta(days=2)

    return None


def parse_previous(s):
    # 处理多少时间以前的
    # 年
    pat = ur"([0-9零一二两三四五六七八九十 ]+)年前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return dt.now().replace(year=dt.now().year - int(intvl), month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # 月
    pat = ur"([0-9零一二两三四五六七八九十 ]+)[个]*月前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return add_months(dt.now(), -int(intvl))
    # 天
    pat = ur"([0-9零一二两三四五六七八九十 ]+)天前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return dt.now() - timedelta(days=int(intvl))
    # 小时
    pat = ur"([0-9零一二两三四五六七八九十 ]+)[个小]*时前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return dt.now() - timedelta(hours=int(intvl))
    # 分钟
    pat = ur"([0-9零一二两三四五六七八九十 ]+)分钟前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return dt.now() - timedelta(minutes=int(intvl))
    # 秒
    pat = ur"([0-9零一二两三四五六七八九十 ]+)秒前"
    m = re.search(pat, s)
    if m:
        intvl = cn2dig(m.group(1).strip())
        return dt.now() - timedelta(seconds=int(intvl))

    return None


if __name__ == '__main__':
    s = u'ab 两年前'

    s = u' 三天前 发表的文章'
    s = u'十三个小时前'
    s = u'90分钟前'
    s = u'匿名 于 大约 3 小时前发布'
    s = u'11 个月前'
    print parse_previous(s)