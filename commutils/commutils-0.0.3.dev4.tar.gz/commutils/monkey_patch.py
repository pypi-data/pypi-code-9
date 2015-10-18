#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# import functools

def as_method_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,func)
    return as_method_of_cls
def as_staticmethod_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,staticmethod(func))
    return as_method_of_cls


class Patcher():
    '''
    register的对象版本, register, functions对应装饰器, _function, 都是引用

    用例:
    reg=Register()

    _functions=reg.functions()
    register=reg.register

    @register
    def new():
        pass

    @register
    def new2():
        pass

    print(_functions)
    '''
    def __init__(self):
        self.method_dict={}
        self.method_list=[]
        self.static_method_dict={}
        self.static_method_list=[]

    # @staticmethod
    def as_method(self,f):
        self.method_dict[f.__name__]=f
        self.method_list.append(f)
        return f

    def as_staticmethod(self,f):
        self.static_method_dict[f.__name__]=f
        self.static_method_list.append(f)
        return f


    def mmp(self,klass):
        '''
        multi monkey patch, with method
        '''
        for i in self.method_list:
            setattr(klass,i.__name__,i)
        for i in self.static_method_list:
            setattr(klass,i.__name__,staticmethod(i))


def monkey_patch(method,klass):
    setattr(klass,method.__name__,method)

def monkey_patch_group(methodlist,klass):
    '''
    multi monkey patch, with method
    '''
    if type(methodlist) is dict:
        print ('dict')
        for i in methodlist:
            setattr(klass,i,methodlist[i])
    else:
        for i in methodlist:
            monkey_patch(klass,i)
            setattr(klass,i.__name__,i)


def mmp(reg,klass):
    '''
    multi monkey patch, with method
    '''
    for i in reg.method_list:
        setattr(klass,i.__name__,i)
    for i in reg.static_method_list:
        setattr(klass,i.__name__,staticmethod(i))
