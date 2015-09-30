import datetime
import dateutil.parser
import requests

class Election(object):

    def __init__(self, json):
        self.absentee_and_provisional = None
        self.cong_dist_level = None
        self.cong_dist_level_status = None
        self.county_level = None
        self.county_level_status = None
        self.direct_links = None
        self.end_date = None
        self.governor = None
        self.house = None
        self.organization = None
        self.portal_link = None
        self.precinct_level = None
        self.precinct_level_status = None
        self.prez = None
        self.primary_note = None
        self.primary_type = None
        self.race_type = None
        self.resource_uri = None
        self.result_type = None
        self.senate = None
        self.special = None
        self.start_date = None
        self.state = None
        self.state_leg = None
        self.state_leg_level = None
        self.state_leg_level_status = None
        self.state_level = None
        self.state_level_status = None
        self.state_officers = None
        self.user_fullname = None

        for k, v in json.items():
            setattr(self, k, v)

    def __unicode__(self):
        return unicode("{election_type} election on {start_date}".format(election_type=self.election_type, start_date=self.start_date))

    def __str__(self):
        return repr("{election_type} election on {start_date}".format(election_type=self.election_type, start_date=self.start_date))

    def generated_filename(self, precinct=None):
        if self.special:
            filename = "__".join([self.start_date.replace('-',''), self.state['postal'].lower(), "special", self.race_type.lower()])
        else:
            filename = "__".join([self.start_date.replace('-',''), self.state['postal'].lower(), self.race_type.lower()])
        if precinct:
            filename = filename+"__precinct.csv"
        else:
            filename = filename+".csv"
        return filename

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
        self.count = None
        self.json = None

    def parse(self):
        r = requests.get(self.url)
        self.json = r.json()['objects']
        self.count = r.json()['meta']['total_count']
        return [Election(e) for e in self.json]
