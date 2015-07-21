# -*- coding: utf-8 -*-
'''
Created on 2012-6-29

@author: lijie.ma
'''
from jiemoutils import funcs

class appinfo(object):
    def __init__(self,accessKeyId,accessKeySecret):
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret

def getDefaultAppInfo():
    pass


def setDefaultAppInfo(accessKeyId,accessKeySecret):
    default = appinfo(accessKeyId,accessKeySecret)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default


aliyun_account = funcs.eval_file('/etc/jiemo/aliyun.py')
setDefaultAppInfo(aliyun_account['access_key'], aliyun_account['access_secret'])

