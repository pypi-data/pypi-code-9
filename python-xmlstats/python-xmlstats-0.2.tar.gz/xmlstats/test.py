#!/usr/bin/python

import sys
from StringIO import StringIO
import urllib
import urllib2
import gzip
import json
import datetime
import dateutil.parser
import httplib
import socket
import ssl

# Replace with your access token
access_token = "4f0057a7-50b5-4831-9cfc-587a00869c41"

# Replace with your bot name and email/website to contact if there is a problem
# e.g., "mybot/0.1 (https://erikberg.com/)"
user_agent = "Robot 1.0 (chezar1995@gmail.com)"

# Some problems have been reported that Python 2.x fails to negotiate the
# correct SSL protocol when connecting over HTTPS. This code forces
# Python to use TLSv1.
# More information and code from http://bugs.python.org/issue11220
class TLS1Connection(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()

        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                ssl_version=ssl.PROTOCOL_TLSv1)

class TLS1Handler(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(TLS1Connection, req)

urllib2.install_opener(urllib2.build_opener(TLS1Handler()))

def main():
    # set the API method, format, and any parameters
    host = "erikberg.com"
    sport = None
    method = "events"
    id = None
    format = "json"
    parameters = {
        'sport': 'nba',
        'date': '20130414'
    }

    # Pass method, format, and parameters to build request url
    url = build_url(host, sport, method, id, format, parameters)

    req = urllib2.Request(url)
    # Set Authorization header
    req.add_header("Authorization", "Bearer " + access_token)
    # Set user agent
    req.add_header("User-agent", user_agent)
    # Tell server we can handle gzipped content
    req.add_header("Accept-encoding", "gzip")

    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        print "Server returned {} error code!\n{}".format(err.code, err.read())
        sys.exit(1)
    except urllib2.URLError, err:
        print "Error retrieving file: {}".format(err.reason)
        sys.exit(1)

    data = None
    if "gzip" == response.info().get("Content-encoding"):
        r= response.read()
        print('Type ', type(r))
        buf = StringIO(r)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    if data:
        print_result(data)

def print_result(data):
    # Parses the JSON content and returns a reference
    # to Events (https://erikberg.com/api/methods/events)
    events = json.loads(data)
    # Use dateutil to parse the ISO 8601 date and return datetime object
    date = dateutil.parser.parse(events['events_date'])
    print "Events on {}\n".format(date.strftime("%A, %B %e, %Y"))
    print "{: <35} {:5} {: >34}".format("Time", "Event", "Status")

    # Loop through each Event (https://erikberg.com/api/objects/event)
    for evt in events['event']:
        time = dateutil.parser.parse(evt['start_date_time'])
        # Get team objects (https://erikberg.com/api/objects/team)
        away_team = evt['away_team']
        home_team = evt['home_team']
        print "{: <12} {: >24} vs. {: <24} {:9}".format(
                time.strftime("%l:%M %p"),
                away_team['full_name'],
                home_team['full_name'],
                evt['event_status'])

# See https://erikberg.com/api/methods Request URL Convention for
# an explanation
def build_url(host, sport, method, id, format, parameters):
    path = "/".join(filter(None, (sport, method, id)));
    url = "https://" + host + "/" + path + "." + format
    if parameters:
        paramstring = urllib.urlencode(parameters)
        url = url + "?" + paramstring
    return url

if __name__ == "__main__":
    main()