"""
A python module to provide methods to write data to Strawpoll's JSON API:
https://strawpoll.me/api/v2/polls

The StrawpollAPIWriter class provides methods for:
* Creating a poll instance
* POSTing data to strawpoll's API
"""
from base.strawpoll_base import StrawpollAPIBase

import requests
import json


class StrawpollAPIWriter(StrawpollAPIBase):
    """
    TODO: Document this class
    """
    # These are the attributes that strawpoll accepts in its API call
    # See: https://github.com/strawpoll/strawpoll/wiki/API
    # The strings have been marked utf-8 for compatibility with json.loads()
    # API_KEYWORDS = frozenset(
    #     [u'title', u'options', u'votes',
    #      u'multi', u'permissive', u'id', u'captcha'])
    # API_ENDPOINT = 'https://strawpoll.me/api/v2/polls'
    # USER_AGENT = 'Strawpoll API Reader'
    # API_POST_HEADERS = {
    #     'Content-Type': 'application/json',
    #     'X-Requested-With': 'StrawpollAPIWriter'
    # }

    def __init__(self, data={}):
        """ Construct self using a dictionary of data """
        super(StrawpollAPIBase, self).__init__()
        for key in data.keys():
            # This actually worked.
            # hasattr -> setattr died with AttributeErrors
            try:
                setattr(self, key, data[key])
            except AttributeError:
                continue

    def post(self):
        """
        Posts the strawpoll object to the strawpoll API and returns a
        Strawpoll object with a valid id attribute. Doesn't handle the case
        where a valid id already exists. If the post is successful a new
        object with overwritten id is returned
        """
        try:
            if len(self.title) == 0 or self.title is None:
                raise AttributeError("Title cannot be blank")
            elif not self.options == 0:
                raise AttributeError("Options cannot be blank")
            else:
                body = json.dumps(self.to_clean_dict())
                response = requests.post(self.API_ENDPOINT,
                                         data=body,
                                         headers=self.API_POST_HEADERS)
                return StrawpollAPIBase.from_json(response.text)
        except StandardError as err:
            print err
