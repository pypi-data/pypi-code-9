# coding=utf8


class_template = """
class _MetaClass(object):
    {}
"""

def metaclass(keys):
    pass

def dict2obj(kv):
    dictclass = dict2class(kv)
    dictclass()
