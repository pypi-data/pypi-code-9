# -*- coding: utf8 -*-
from __future__ import print_function
from os.path import abspath, dirname, join
from math import sqrt
from pytz import timezone
from factory import open_db_file, make_searcher, searcher_in_continent


class Shared:
	is_db_loaded = False
	positions = []
	names = []

def load_default_db():
	if Shared.is_db_loaded:
		return
	try:
		Shared.positions = []
		with open_db_file() as dbfile:
			i = 0
			for line in dbfile:
				parsed = line.split()
				t = [float(parsed[0]), float(parsed[1])]
				Shared.positions.append(t)
				Shared.names.append(parsed[2])
				i += 1
		Shared.is_db_loaded = True
	except:
		raise
		Shared.is_db_loaded = False

""" Given a longitude and latitude calculate
the nearest place in the database and return
its timezone """
def tz_from_loc(lat=0, lon=0):
	if not Shared.is_db_loaded:
		load_default_db()
	lower_distance = 9999999
	index = 0
	i = 0
	lastrawdif = 0

	if Shared.is_db_loaded == False:
		return (None, None, )
		
	for location in Shared.positions:
		lt, ln = location
		ltdif = abs(lt - lat)
		lndif = abs(ln - lon)
		dtdif = sqrt((ltdif * ltdif) + (lndif * lndif))
		if dtdif < lower_distance:
			lower_distance = dtdif
			lastrawdif = dtdif
			index = i
		i += 1

	return timezone(Shared.names[index])


if __name__ == '__main__':
	import time
	n = 300
	print("Running test\n" + "-" * 30)
	t = time.time()
	sr = searcher_in_continent('America')
	for i in range(n):
		# Hermosillo
		tz = sr.timezone_at(29.757512, -111.070278)
	print("time spent: %.5f seconds" % (time.time() - t))
	#print("time zone: %s" % tz)
