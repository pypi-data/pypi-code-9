''' Copyright 2015 Neokami GmbH. '''

from dicttoxml import dicttoxml

class Base():
	API_BASE = 'https://api.neokami.io'
	SDK_VERSION = '0.2'
	SDK_LANG = 'python'

	def getUrl(self, path):
		return self.API_BASE + path


	def toXML(self, array):
		return dicttoxml(array, attr_type=False)
