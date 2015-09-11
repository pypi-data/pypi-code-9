#!C:\Python27\\python.exe
#coding=utf-8
import re,sys
'''html页面内容处理'''
def getAllUrls(html):
	'''获取所有的url链接'''
	urls = re.findall(r'<a.*?href="(.*?)".*?>', html)
	return urls