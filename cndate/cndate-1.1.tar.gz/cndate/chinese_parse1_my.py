# coding:utf8
"""
u'50分鐘前',
    u'匿名 於 大約 3 小時前發佈',
    u'匿名 於 36 分鐘前發佈']
    匿名 於 一天前發佈
    匿名 於一天前發表
    於4 天前發表
    匿名 於大約一個月前發表

"""
import re
import datetime
from utils import cn2dig


def parse_datetime(msg):
    # m = re.match(ur"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?", msg)
    m = re.search(ur"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?", msg)
    print u'找到的group: ', m.groups(), type(m.groups())
    print type(m)
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
        print u'group(0): ', m.group(0)
        params = {}
        for name in res:
            if res[name] is not None and len(res[name]) != 0:
                print 'name: ', name, 'val: ', res[name]
                params[name] = int(cn2dig(res[name][:-1]))
                # print 'name: ', name, 'val: ', params[name]
        target_date = datetime.datetime.today().replace(**params)
        is_pm = m.group(4)
        if is_pm is not None:
            if is_pm == u'下午' or is_pm == u'晚上':
                hour = target_date.time().hour
                if hour < 12:
                    target_date = target_date.replace(hour=hour+12)
        return target_date
    else:
        return None

if __name__ == "__main__":
    '''
    print parse_datetime(None)
    print parse_datetime(u"两点30分")
    print parse_datetime(u"7点")
    print parse_datetime(u"五分")
    print parse_datetime(u"七点五分")
    print parse_datetime(u"七点零五分")
    print parse_datetime(u"9点04分")
    print parse_datetime(u"下午9点04分")
    print parse_datetime(u"6月三十日04分")
    print parse_datetime(u"1995年6月10号下午3点41分50秒")


    # print parse_datetime(u'匿名 於 一天前發佈')
    print parse_datetime(u"1998年1月8日")
    print parse_datetime(u"两分钟前")
    print parse_datetime(u'2015 年 09 月 28 日 ')
    '''
    print parse_datetime(u"1995年6月10号下午3点41分50秒")
    # print cn2dig(u'四千五十五')

    pass
