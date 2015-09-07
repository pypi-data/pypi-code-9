# -*- coding: utf8 -*-
from __future__ import print_function
from os.path import abspath, dirname, join
from math import sqrt
from pytz import timezone
from factory import open_db_file


class Shared:
	is_db_loaded = False
	positions = []
	names = []

def load_default_db():
	import numpy
	if Shared.is_db_loaded:
		return
	try:
		Shared.positions = numpy.array([[0, 0] for x in range(22643)],
						   numpy.float32)
		with open_db_file() as dbfile:
			i = 0
			for line in dbfile:
				parsed = line.split()
				Shared.positions[i] = [float(parsed[0]), float(parsed[1])]
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
	import numpy
	if not Shared.is_db_loaded:
		load_default_db()
	lower_distance = 9999999
	index = 0
	i = 0
	lastrawdif = 0

	if Shared.is_db_loaded == False:
		return (None, None, )
		
	for location in Shared.positions:
		lt = location[0]
		ln = location[1]
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
	load_default_db()
	n = 50
	print("Running test\n" + "-" * 30)
	t = time.time()
	for i in range(n):
		# Hermosillo
		tz = tz_from_loc(29.757512, -111.070278)
	print("time spent: %.5f seconds" % (time.time() - t))
	#print("time zone: %s" % tz)
