#!/usr/bin/env python

import json
import urllib2
import base64


class Request2(urllib2.Request):
    def __init__(self, url, method, data=None, headers={}):
        self._method = method
        urllib2.Request.__init__(self, url=url, headers=headers, data=data)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)


class GnipError(Exception):
    pass


class GnipPowerTrack(object):
    def __init__(self, account_name=None, username=None, passwd=None,
                 stream_label="prod", data_source='twitter'):

        self.GNIP_ACCOUNT_NAME = account_name
        self.GNIP_STREAM_LABEL = stream_label
        self.GNIP_DATA_SOURCE = data_source
        self.GNIP_AUTH_STRING = base64.encodestring('%s:%s' % (username,
                                                               passwd)).replace('\n', '')

    def addRule(self, tag, value):
        url = self._buildRulesURL()
        rules_str = """{"rules": [{"value":'%(value)s',"tag":'%(tag)s'}]}""" % \
                    {"tag": tag,
                     "value": value.replace("'", "\\'")}

        print rules_str

        req = Request2(url, 'POST', data=rules_str)
        req.add_header('Content-type', 'application/json')
        req.add_header("Authorization", "Basic %s" % self.GNIP_AUTH_STRING)

    def removeRule(self, rule):
        url = self._buildRulesURL()

        rules_str = '{"rules": [{"value":' + rule + '}]}'
        print rules_str

        req = Request2(url, 'DELETE', data=rules_str)

        req.add_header('Content-type', 'application/json')
        req.add_header("Authorization", "Basic %s" % self.GNIP_AUTH_STRING)
        response = urllib2.urlopen(req)
        print response.read()

    def getRules(self):
        url = self._buildRulesURL()
        req = Request2(url, 'GET')
        req.add_header('Content-type', 'application/json')
        req.add_header("Authorization", "Basic %s" % self.GNIP_AUTH_STRING)

        try:
            response = urllib2.urlopen(req)
            return json.loads(response.read()).get("rules")
        except:
            return None

    def _buildRulesURL(self):
        url = ("https://api.gnip.com:443"
               "/accounts/%(account_name)s"
               "/publishers/%(data_source)s"
               "/streams/track/%(stream_label)s"
               "/rules.json") % {"account_name": self.GNIP_ACCOUNT_NAME,
                                 "data_source": self.GNIP_DATA_SOURCE,
                                 "stream_label": self.GNIP_STREAM_LABEL}

        return url
