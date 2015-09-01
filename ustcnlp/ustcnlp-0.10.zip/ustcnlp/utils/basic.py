# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

TYPE_UNICODE = type(u'')
TYPE_BASESTRING = type(b'')

####工具类######
class BaseClass(object):
    def __init__(self, **args):
        for k, v in args.items():
            self.__setattr__(k, v)

def uuid_gen(s):
    """
    使用uuid.uuid3生成一个uuid
    """
    import uuid
    if type(s) == TYPE_UNICODE:
        try:
            s = s.encode('utf8')
        except:
            try:
                s = s.encode('gbk')
            except:
                pass
    return uuid.uuid3(uuid.NAMESPACE_OID, s)

def it_filter(it, flfun):
    '''
    迭代器过滤
    '''
    for t in it:
        if flfun(t):
            yield t

def dup_free(items):
    '''
    返回去除重复元素后的列表
    '''
    return list(set(items))


if __name__ == '__main__':
    pass
