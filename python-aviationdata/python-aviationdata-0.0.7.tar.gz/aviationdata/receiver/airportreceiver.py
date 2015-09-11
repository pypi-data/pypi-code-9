import requests
from . import Receiver
import csv
from cStringIO import StringIO

class AirportReceiver(Receiver):
    _url = 'http://ourairports.com/data/airports.csv'

    def __init__(self, icaoIdentifiers = None):
        super(AirportReceiver, self).__init__(icaoIdentifiers)

    def receive(self):
        airports_raw = self._getData(self._url)
        if self._icaoIdentifiers:
            airports_raw = filter(lambda x: (x['ident'].lower() in self._icaoIdentifiers), airports_raw)

        frequencies_raw = self._frequencies()
        runways_raw = self._runways()

        for row in airports_raw:
            row['longitude_deg'] = float(row['longitude_deg'])
            row['latitude_deg'] = float(row['latitude_deg'])
            row['id'] = int(row['id'])
            row['elevation_ft'] = int(row['elevation_ft']) if row['elevation_ft'] else None

            row['frequencies'] = filter(lambda x: (int(x['airport_ref']) == row['id']), frequencies_raw)
            row['runways'] = filter(lambda x: (int(x['airport_ref']) == row['id']), runways_raw)

            yield row

    def _convertToList(self, dictreader):
        x = []
        for i in dictreader:
            x.append(i)
        return x

    def _frequencies(self):
        url = "http://ourairports.com/data/airport-frequencies.csv"
        return self._getData(url=url)

    def _runways(self):
        url = "http://ourairports.com/data/runways.csv"
        return self._getData(url=url)

    def _getData(self, url):
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            return False
        data = StringIO(r.text.encode('utf-8'))
        return self._convertToList(csv.DictReader(data))
