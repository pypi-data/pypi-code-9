# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:23:24 2015

@author: fly
"""
import base64


def parser(url):
    """解析迅雷下载链接"""
    protocol, url = url.split('://')
    if protocol.lower() == 'thunder':
        url = base64.b64decode(url)
        url = url[2:-2]
        return url


def test():
    url = 'thunder://QUFmdHA6Ly9nOmdAZHguZGwxMjM0LmNvbTo4O' \
          'DA4LyVFOCVCNSVBNCVFOSU4MSU5M0JEJUU1JTlCJUJEJUU3J' \
          'UIyJUE0JUU1JThGJThDJUU4JUFGJUFEJUU0JUI4JUFEJUU1J' \
          'UFEJTk3WyVFNyU5NCVCNSVFNSVCRCVCMSVFNSVBNCVBOSVFNS' \
          'VBMCU4Mnd3dy5keTIwMTguY29tXS5ta3ZaWg=='
    return parser(url)

if __name__ == '__main__':
    print(test())
