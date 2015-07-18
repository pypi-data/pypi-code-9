#!/usr/bin/env python

import re
import json
import urllib2
import base64

from exceptions import GnipException, GnipUnauthorizedException


class Request2(urllib2.Request):
    def __init__(self, url, method, data=None, headers={}):
        self._method = method
        urllib2.Request.__init__(self, url=url, headers=headers, data=data)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)


class GnipPowerTrack(object):
    def __init__(self, account_name=None, username=None, passwd=None,
                 stream_label="prod", data_source='twitter'):

        self.GNIP_ACCOUNT_NAME = account_name
        self.GNIP_STREAM_LABEL = stream_label
        self.GNIP_DATA_SOURCE = data_source
        self.GNIP_AUTH_STRING = base64.encodestring('%s:%s' % (username,
                                                               passwd)).replace('\n', '')

    def addRule(self, tag, value):
        """ Adds a rule into a Gnip PowerTrack Stream

            @param tag: The tag that identifies the rule
            @type tag: string

            @param value: The rule to be added into the PowerTrack Stream
            @type value: string

            @return: True if succesful. Raises an error otherwise.
            @throws: :class: ~exceptions.GnipException, :class: ~exceptions.GnipUnauthorizedException
        """

        if value == "":
            raise ValueError("Value/Rule cannot be blank!")

        rules = {"rules": [{"value": value, "tag": tag}]}
        rules_json = json.dumps(rules)
        self._sendPowertrackRequest(method="POST", data=rules_json)
        return True

    def removeRule(self, value):
        """ Removes a rule from a Gnip PowerTrack Stream

            @param value: The value of the rule to be removed
            @type value: string

            @return: True if succesful
        """

        if value == "":
            raise ValueError("Value/Rule cannot be blank!")

        rules = {"rules": [{"value": value}]}
        rules_json = json.dumps(rules)
        self._sendPowertrackRequest(method="DELETE", data=rules_json)
        return True

    def getRules(self):
        """ Retrieves all rules associated with a PowerTrack Stream

            @return: A python list containing python dictionaries of
                     the existing rules
        """

        response = self._sendPowertrackRequest(method="GET")
        return json.loads(response).get("rules")

    def _sendPowertrackRequest(self, method, data=None):
        """ Definition for sending an HTTP Request to the PowerTrack API Endpoint

            @param method: The HTTP method to use
            @type method: string

            @param data: The JSON data payload to send to the endpoint
            @type data: A JSON string

            @return: The results for urllib2 response.read() if status code is either 201 or 200,
                     throws an error otherwise

        """
        url = self._buildRulesURL()
        req = Request2(url, method, data=data)
        req.add_header('Content-type', 'application/json')
        req.add_header("Authorization", "Basic %s" % self.GNIP_AUTH_STRING)

        try:
            response = urllib2.urlopen(req)
            code = response.getcode()

            if code == 201 or code == 200:
                return response.read()
            else:
                raise GnipException("Unknown resonse from GNIP")

        except urllib2.HTTPError, e:
            error_code = e.getcode()

            if error_code == 401:
                raise GnipUnauthorizedException("Invalid Credentials")
            else:
                raise e

    def _buildRulesURL(self):
        url = ("https://api.gnip.com:443"
               "/accounts/%(account_name)s"
               "/publishers/%(data_source)s"
               "/streams/track/%(stream_label)s"
               "/rules.json") % {"account_name": self.GNIP_ACCOUNT_NAME,
                                 "data_source": self.GNIP_DATA_SOURCE,
                                 "stream_label": self.GNIP_STREAM_LABEL}

        return url
