import urllib2
import json
import numpy as np
"""
Send API call to metanumber server (designated via the URL variable). The equation is appended (per the parameters of the API call), and the result is returned / parsed.
"""
def call(equation):
	url = 'http://tyson.rci.sc.edu/metanumber/api/v1.0/engine/'	#MN server address
	equation = str(equation).replace("/", "|")				#parse equation for division
	requestURL = url + equation					#concatenate URL and equation for full API call
	returnValue = json.loads(urllib2.urlopen(requestURL).read())	#get return value
	#print returnValue['result']					#parse and print
	return returnValue['result']
