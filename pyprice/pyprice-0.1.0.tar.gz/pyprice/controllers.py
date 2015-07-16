# -*- coding:utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


def search(keyword):
	url = "".join(('https://s.yimg.com/aq/autoc?query=', keyword, '&region=US&lang=en-US&callback=YAHOO.util.ScriptNodeDataSource.callbacks'))
	return json.loads(requests.get(url).text[42:-1])


def index(keyword):
	url = "".join(('http://finance.yahoo.com/q?s=', keyword))
	html = BeautifulSoup(requests.get(url).text, 'html.parser')
	print(html.findAll('span'))
	#return html.find('span', id='priceLegend'), html.find('span', id='legendPriceChange'), html.find('span', id='legendPctChange')#html.find('div', id='legendData').find('div', 'symbol-name'), html.find('span', id='priceLegend'), html.find('span', id='legendPriceChange'), html.find('span', id='legendPctChange')
	

def test(keyword):
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
		'Connection': 'keep-alive',
		'Host': 'finance.yahoo.com',
		'Referer': 'http://finance.yahoo.com/q?s=^KS11',
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
		'X-Requested-With': 'XMLHttpRequest',
		'Cookie': 'B=52o6gn9al00dn&b=3&s=ko; ywandp=1000911397279%3A4125726577; fpc=1000911397279%3AZUk4bVZE%7C%7C; ypcdb=93e8aebc5f16756a5402764abbdbca4e; ywadp115488662=3024871490; GG=eyJmaW5hbmNlLnwiOnsidCI6MTQzNzEwMTY4Nn19; yvapF=%7B%22cc%22%3A1%2C%22rcc%22%3A1%2C%22vl%22%3A1.318%2C%22rvl%22%3A1.318%2C%22al%22%3A1%7D; PRF==undefined&t=%5EKS11'
	}
	url = "".join((
		'http://finance.yahoo.com/__td_finance_api/resource/charts;comparisonTickers=;indicators=quote;queryString={"s":"', 
		keyword, 
		'"};range=1d;rangeSelected=;ticker=', 
		keyword, 
		';useMock=false?crumb=0lVU/cVsiHK&lang=en-US&region=US'
	))
	return requests.get(url, headers=headers).text	
