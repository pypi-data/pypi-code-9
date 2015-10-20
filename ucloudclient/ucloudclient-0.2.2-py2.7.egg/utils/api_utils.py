# -*- coding:utf-8 -*-
import hashlib
import time


region = "cn-north-03"
region = "cn-east-01"
region = "hk-01"
region = "us-west-01"
'''
数据中心名称	API名称	数据中心网络带宽线路
北京BGP-A	cn-north-01	Bgp: BGP线路
北京BGP-B	cn-north-02	Bgp: BGP线路
北京BGP-C	cn-north-03	Bgp: BGP线路
华东双线	cn-east-01	Duplet: 双线, Unicom: 网通, Telecom: 电信
华南双线	cn-south-01	Duplet: 双线, Unicom: 网通, Telecom: 电信
亚太	hk-01	International: 国际线路
北美	us-west-01	International: 国际线路
'''


def get_token(private_key, params):
    items = params.items()
    items.sort()

    params_data = ""
    for key, value in items:
        params_data = params_data + str(key) + str(value)
    params_data = params_data + str(private_key)

    sign = hashlib.sha1()
    sign.update(params_data)
    signature = sign.hexdigest()

    return signature


def get_formate_time(now):
    if now:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    return ''
