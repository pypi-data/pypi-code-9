# coding:utf-8
"""
时间:2015/9/30
说明:
"""
import re
import calendar
from datetime import datetime
from dateutil.parser import parse


UTIL_CN_NUM = {
                u'零': 0,
                u'一': 1,
                u'二': 2,
                u'两': 2,
                u'三': 3,
                u'四': 4,
                u'五': 5,
                u'六': 6,
                u'七': 7,
                u'八': 8,
                u'九': 9,
                }
UTIL_CN_UNIT = {
                u'十': 10,
                u'百': 100,
                u'千': 1000,
                u'万': 10000,
                }


# dateutil库能处理的类型
DUTIL_LIST = [
    u"\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2} [AM|PM|am|pm]",
    u"\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}",

    u"\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2} [AM|PM|am|pm]",
    u"\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}",

    u'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2} [AM|PM|am|pm]'
    u'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}',  # 7/2/2015 0:05

    u'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} [AM|PM|am|pm]',
    u'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2}',

    u'\d{1,2}/\d{1,2}/\d{2,4}',
]


ZH_LIST = [
    u""
]


def cn2dig(src):
    """
    把中文转换成数字， 十五变成 15
    """
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return m.group(0)
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num*unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return str(rsl)


def add_months(sourcedate, months):
    """
    只添加月份, 会省掉天，时分等
    :param sourcedate:
    :param months:
    :return:
    """
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    # return datetime.date(year, month, day)
    return datetime(year=year, month=month, day=day)


def totimestamp(dt, epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def parse_chinese(s):
    """
    只解析包含中文字符的日期
    """
    m = re.search(ur"([0-9零一二两三四五六七八九十 ]+年)?([0-9一二两三四五六七八九十 ]+月)?([0-9一二两三四五六七八九十 ]+[号日])?([上下午晚早 ]+)?([0-9零一二两三四五六七八九十百 ]+[点:\.时])?([0-9零一二三四五六七八九十百 ]+分?)?([0-9零一二三四五六七八九十百 ]+秒)?", s)
    # print u'找到的group: ', m.groups(), type(m.groups())

    if m.group(0) is not None:
        res = {
            "year": m.group(1),
            "month": m.group(2),
            "day": m.group(3),
            "hour": m.group(5) if m.group(5) is not None else '00',
            "minute": m.group(6) if m.group(6) is not None else '00',
            "second": m.group(7) if m.group(7) is not None else '00',
            # "microsecond": '00',
            }
        '''
        print u'找到的值:'
        for k, v in res.items():
            print k, '-', v'''
        params = {}
        for name in res:
            if res[name] is not None and len(res[name]) != 0:
                # 找出解析到的年月日..如'2015 年 09 月 28 日' 解析出各个字段，但是各个字段都有可能间隔空格
                valid_str = res[name].strip()[:-1].strip()
                # print 'valid_str: ', valid_str
                params[name] = int(cn2dig(valid_str))
                # print 'name: ', name, 'val: ', params[name]
        target_date = datetime.today().replace(**params)
        is_pm = m.group(4)
        if is_pm is not None:
            is_pm = is_pm.strip()
            if is_pm == u'下午' or is_pm == u'晚上':
                hour = target_date.time().hour
                if hour < 12:
                    target_date = target_date.replace(hour=hour+12)
        return target_date.replace(microsecond=0)
    else:
        return None


def parse_chinese_odds(s):
    """
    处理一些特殊的格式
    :param s:
    :return:
    """
    # ------- 2015/10/5 下午 07:02:53 --------------
    if u'上午' in s:
        s = s.replace(u'上午', u' ')
        s += u' AM'

    if u'下午' in s:
        s = s.replace(u'下午', u' ')
        s += u' PM'

    return parse(s)

if __name__ == '__main__':
    # s = totimestamp(datetime.now())
    # print parse_chinese(None)
    '''
    print parse_chinese(u"两点30分")
    print parse_chinese(u"7点")
    print parse_chinese(u"五分")
    print parse_chinese(u"七点五分")
    print parse_chinese(u"七点零五分")
    print parse_chinese(u"9点04分")
    print parse_chinese(u"下午9点04分")
    print parse_chinese(u"20号")
    print parse_chinese(u"6月三十日04分")
    print parse_chinese(u"1995年6 月10 号 下午 3 点41 分50 秒")

    # print parse_datetime(u'匿名 於 一天前發佈')
    print parse_chinese(u"1998年1月8日")
    print parse_chinese(u"两分钟前")
    print parse_chinese(u'2015 年 09 月 28 日 ')'''

    # print parse_chinese(u'2015/10/5 下午 07:02:53  '.strip())

    s = u'2015/10/5 下午 07:02:53'
    print parse_chinese_odds(s)
    # print type(s)
