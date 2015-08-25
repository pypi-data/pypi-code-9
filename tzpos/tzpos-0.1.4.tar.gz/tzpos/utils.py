# -*- coding: utf8 -*-
from __future__ import print_function
from os.path import abspath, dirname, join
from math import sqrt
from pytz import timezone


base_dir = dirname(abspath(__file__))
filename = join(base_dir, "tzposdb.data")

# Lista de posiciones
positions = []

# Lista de nombres de timezones
names = []

is_db_loaded = False

# Precargar la lista de datos
try:
	with open(filename, 'rb') as dbfile:
		for line in dbfile:
			parsed = line.split()
			t = (float(parsed[0]), float(parsed[1]))
			positions.append(t)
			names.append(parsed[2])
	is_db_loaded = True
except:
	raise
	is_db_loaded = False

""" Given a longitude and latitude calculate
the nearest place in the database and return
its timezone """
def tz_from_loc(lat=0, lon=0):
	lower_distance = 9999999
	index = 0
	i = 0
	lastrawdif = 0

	if is_db_loaded == False:
		return (None, None, )
		
	for location in positions:
		lt, ln = location
		ltdif = abs(lt - lat)
		lndif = abs(ln - lon)
		dtdif = sqrt((ltdif * ltdif) + (lndif * lndif))
		if dtdif < lower_distance:
			lower_distance = dtdif
			lastrawdif = dtdif
			index = i
		i += 1

	return timezone(names[index]) + 'simet'


if __name__ == '__main__':
	print("Running test\n" + "-" * 30)
	print(tz_from_loc(29.757512, -111.070278)) # Hermosillo
