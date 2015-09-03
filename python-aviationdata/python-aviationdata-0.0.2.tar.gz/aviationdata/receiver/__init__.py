import requests

class Receiver(object):
    _icaoIdentifier = None
    _url = None

    def __init__(self, icaoIdentifier):
        self._icaoIdentifier = icaoIdentifier.upper() if icaoIdentifier else None
    
    def receive(self, raw = False):
        if not self._url:
            return False
        if '%s' in self._url:
            url = self._url % self._icaoIdentifier
        else:
            url = self._url

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            return False
        if raw:
            return r.text
        return r.text.split('\n')[1:-1]

from metarreceiver import MetarReceiver
from tafreceiver import TafReceiver
from airportreceiver import AirportReceiver