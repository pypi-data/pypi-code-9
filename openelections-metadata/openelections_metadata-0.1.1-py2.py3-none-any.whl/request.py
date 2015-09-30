import datetime
import dateutil.parser
import requests
from metadata.election import Election

class Request(object):

    def __init__(self, state_postal, start_date=None, end_date=None, offset=0):
        if start_date and end_date:
            url = "http://openelections.net/api/v1/election/?format=json&state__postal=%s&start_date__gte=%s&end_date__lte=%s&offset=%s" % (state_postal, start_date, end_date, offset)
        elif start_date:
            url = "http://openelections.net/api/v1/election/?format=json&state__postal=%s&start_date__gte=%s&offset=%s" % (state_postal, start_date, offset)
        elif end_date:
            url = "http://openelections.net/api/v1/election/?format=json&state__postal=%s&end_date__lte=%s&offset=%s" % (state_postal, end_date, offset)
        else:
            url = "http://openelections.net/api/v1/election/?format=json&state__postal=%s&offset=%s" % (state_postal, offset)
        self.url = url
        self.state = state_postal
        self.offset = offset
        self.start_date = start_date
        self.end_date = end_date
        self.json = self.get_json()['objects']
        self.elections = [Election(e) for e in self.json]

    def get_json(self):
        r = requests.get(self.url)
        return r.json()
