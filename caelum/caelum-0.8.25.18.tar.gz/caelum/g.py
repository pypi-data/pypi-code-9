import csv
'USAF,Site Name,State,Latitude,Longitude,TZ,Elev,Class,Pool'
'region,country,weather_station,station_code,data_format,url'

from geopy import geocoders
geocoder = geocoders.GoogleV3()

f = csv.DictReader(open('./eere.csv'))
for i in f:
    try:
        if i['region'] != '4' and i['region'] != 'problem':
            loc = geocoder.geocode(i['country'] +', ' + i['weather_station'])
            tz = geocoder.timezone(loc.point)
            b = [i['station_code'], i['weather_station'], i['country'],
                loc.latitude, loc.longitude, tz.zone, loc.altitude, 'IV']
            print ', '.join([str(i) for i in b])
    except Exception as e:
        print e

