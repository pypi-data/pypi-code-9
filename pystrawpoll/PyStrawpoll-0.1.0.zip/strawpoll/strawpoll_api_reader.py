"""
A python module to provide methods to read data from existing polls using
Strawpoll's JSON API (https://strawpoll.me/api/v2/polls).

The StrawpollAPIReader class provides methods for:
* Capturing all poll data in an instance
* Performing basic options such as normalizing votes for each option
* Finding the winner / loser
"""

from __future__ import division
from base.strawpoll_base import StrawpollAPIBase

import requests
import json


class StrawpollAPIReader(StrawpollAPIBase):
    """
    TODO: Document this class
    """
    def __init__(self, data={}):
        """ Construct self using a dictionary of data """
        super(StrawpollAPIReader, self).__init__()
        for key in data.keys():
            # This actually worked.
            # hasattr -> setattr died with AttributeErrors
            try:
                setattr(self, key, data[key])
            except AttributeError:
                # Log this?
                continue

    @classmethod
    def from_json(cls, json_string):
        """
        Constructs a poll instance from a JSON string
        returned by strawpoll.me API
        """
        api_response = json.loads(json_string)
        response_keys = set(api_response.keys())
        if response_keys.issubset(cls.API_KEYWORDS):
            return cls(data=api_response)

    @classmethod
    def from_apiv2(cls, id):
        """ Constructs a poll instance using a strawpoll id """
        response = requests.get(cls.API_ENDPOINT + str(id))
        return cls.from_json(response.text)

    @classmethod
    def from_url(cls, url):
        """
        Constructs a poll instance using a strawpoll url, that matches:
        ^https?://strawpoll.me/[1-9][0-9]*/?r?
        Issues: Still matches 'http://strawpoll.me/1r', but ignores the r at
        the very end
        """
        matches = cls.URL_PATTERN.match(url)
        if matches is not None:
            # Note: we are actually passing a str and not an int
            return cls.from_apiv2(matches.group('id'))
