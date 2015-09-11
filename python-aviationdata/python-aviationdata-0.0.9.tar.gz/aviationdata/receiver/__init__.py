import requests

class Receiver(object):
    _icaoIdentifiers = None
    _url = None

    def __init__(self, icaoIdentifiers=None):
        self._icaoIdentifiers = map(lambda x: x.lower(), icaoIdentifiers) if isinstance(icaoIdentifiers, (list,)) else None
    
    def receive(self, raw = False):
        if not self._url:
            return

        for icao in self._icaoIdentifier:
            if '%s' in self._url:
                url = self._url % icao
            else:
                url = self._url

            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                continue
            if raw:
                yield r.text
            else:
                yield r.text.split('\n')[1:-1]

from metarreceiver import MetarReceiver
from tafreceiver import TafReceiver
from airportreceiver import AirportReceiver
from hbaircraftreceiver import HbAircraftReceiver