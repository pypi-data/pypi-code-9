__author__ = 'tspycher'

import requests
from bs4 import BeautifulSoup
from slugify import slugify

from . import Receiver

class HbAircraftReceiver(Receiver):
    _url = 'http://www.bazl.admin.ch/experten/luftfahrzeuge/luftfahrzeugregister/index.html'

    def __init__(self, identifiers = None):
        pass

    def receive(self):
        imatr = self.getAllCallsigns()

        for i in imatr:
            soup = BeautifulSoup(self._getData(i), 'html.parser')
            data = self._parseTable(soup.find("table", title="Search results Aircraft Registry"))
            if not data:
                continue
            yield data

    def getAllCallsigns(self):
        chars = 'abcdefghijklmnopqrstuvwxyz'

        list = []
        for x1 in chars:
           for x2 in chars:
               for x3 in chars:
                   list.append("%s%s%s" % (x1, x2, x3))
        return list

    def _parseTable(self, table):
        records = {}
        for row in table.findAll('tr'):
            col = row.findAll('td')
            if not col:
                continue
            key = slugify(str(col[0].text.encode('utf-8')))
            value = str(col[1].text.encode('utf-8'))
            if key in ['no-of-seats', 'year-of-manufacture', 'max-take-off-mass-kg']:
                value = int(value)

            records[key] = value
        return None if not records else records

    def _getData(self, imatriculation):
        r = requests.get(self._url, params={'lang': 'en', 'lfrSucheDetailKnz':'HB-%s' % str(imatriculation).capitalize()})
        if r.status_code != requests.codes.ok:
            return False
        return r.text.encode('utf-8')

