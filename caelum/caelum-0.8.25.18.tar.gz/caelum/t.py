from tools import parse_noaa_line, closest_eere
from tools import eere_station
from geopy.distance import great_circle


import csv

with open('./inswo-stns.txt') as foo:
    foo.readline()
    foo.readline()
    while foo:
        b = parse_noaa_line(foo.readline())
        try:
            s = eere_station(b['station_code'])
            c, n = closest_eere(b['LAT'],b['LON'])
            if b['station_code'] != c:
                #print 'different station', b, c, n
                d = great_circle((b['LAT'],b['LON']),(s['latitude'],s['longitude']))
                if d > 100:
                    print b['station_code'], c, s['station_code'], s['weather_station'], n, d
                #print b
        except:
            #print 'not found'
            pass
