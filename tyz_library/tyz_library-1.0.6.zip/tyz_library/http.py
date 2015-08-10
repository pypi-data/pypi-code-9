#!C:\Python27\\python.exe
#coding=utf-8
'''
http相关请求函数
'''
import urllib2
import socket
import chardet
from tyz_library.myException import MyException 
socket.setdefaulttimeout(10)
def getRemote(url):
	'''获取远程html内容'''
	try:
		req = urllib2.urlopen(url)
	except urllib2.URLError:
		return ''
	html = req.read()
	return html

def convertUnicode(html):
	'''将未知编码的html内容转换成unicde编码'''
	encodeDict = chardet.detect(html)
	if encodeDict['encoding'] == 'utf-8' or encodeDict['encoding'] == 'UTF-8':
		return html.decode('utf-8', 'ignore')
	elif encodeDict['encoding'] == 'gbk' or encodeDict['encoding'] == 'GBK':
		return html.decode('gbk', 'ignore')
	elif encodeDict['encoding'] == 'gb2312' or encodeDict['encoding'] == 'GB2312':
		return html.decode('gb2312', 'ignore')
	else:
		raise MyException, 'uncatch coding!'

	