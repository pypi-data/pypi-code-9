import re
from . import Receiver

class AirportReceiver(Receiver):
    _url = 'http://www.aviationweather.gov/static/adds/metars/stations.txt'

    def __init__(self, icaoIdentifier = None):
        super(AirportReceiver, self).__init__(icaoIdentifier)

    def receive(self):
        data = super(AirportReceiver, self).receive()
        airports = []

        for x in data:
            if self._icaoIdentifier:
                match = re.search(r'%s' % self._icaoIdentifier, x)
            else:
                match = re.match(r'^\w{2}.*(\w{4}).*(\d{2,3}\s\d{2,3}[N,S]\s*\d{2,3}\s\d{2,3}[W,E]).*$', x)
            if match:
                airport_details = self._parse_airport(x)
                if airport_details:
                    airports.append(airport_details)
        return airports

    def _parse_airport(self, airport):
        icao = re.findall(r'\s[A-Z]{4}\s', airport)
        if not icao:
            return
        icao = str(icao[-1]).replace(' ', '')

        lat = self._convertGeo(re.search(r'\d{2,3}\s\d{2,3}[N,S]', airport).group(0))
        long = self._convertGeo(re.search(r'\d{2,3}\s\d{2,3}[W,E]', airport).group(0))
        country = re.search(r'\w{2}$', airport).group(0)
        return {'icao':icao, 'latitude': lat, 'longitude':long, 'country':country, '_raw': airport}

    def _convertGeo(self, orig):
        comp_dir = -1.0 if str(orig[-1:]).lower() in ('w', 's') else 1.0
        non_decimal = re.compile(r'[^\d ]+')
        degs, mins = str(non_decimal.sub('', orig)).split(" ")
        return (float(degs) + (float(mins) / 60)) * comp_dir
