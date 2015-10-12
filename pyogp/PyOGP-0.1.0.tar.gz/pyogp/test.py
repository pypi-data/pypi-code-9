# -*- coding:utf-8 -*-
from pyogp import PyOGP

url = "http://blog.naver.com/mjl0906/220310129634"
a = PyOGP(url=url)
# print a.url
a.crawl(url)
