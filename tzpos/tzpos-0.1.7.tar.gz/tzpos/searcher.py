from math import sqrt
from pytz import timezone


class Searcher(object):
	__slots__ = ['rawdb', 'tznames']

	def __init__(self):
		self.rawdb = []
		self.tznames = []

	def timezone_at(self, lat, lon):
		lower_distance = 9999999
		index = 0
		i = 0
		lastrawdif = 0
			
		for location in self.rawdb:
			lt, ln = location
			ltdif = abs(lt - lat)
			lndif = abs(ln - lon)
			dtdif = sqrt((ltdif * ltdif) + (lndif * lndif))
			if dtdif < lower_distance:
				lower_distance = dtdif
				lastrawdif = dtdif
				index = i
			i += 1

		return timezone(self.tznames[index])
