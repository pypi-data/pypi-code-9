#!/bin/python

import requests,xmltodict,json,sys

def getjson(user): #pega json do gihub
	url = 'https://api.github.com/users/' + str(user)
	dump = requests.get(url)
	dct = json.loads(dump.content)
	return dct

def junparse(s): #transforma dict(do json) em xml	
	xml = xmltodict.unparse({'user' : s}, pretty = True)
	return xml

if __name__ == '__main__':
	g = getjson(sys.argv[1])
	j = junparse(g)
	print j

