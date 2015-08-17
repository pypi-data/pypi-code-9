# coding:utf-8

import time


class Snote(object):
    def __init__(self, data, token):
        self._obj, self._timestamp, self._tag = data
        self._token = token

    @property
    def obj(self):
        return self._obj

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def is_valid(self):
        return self._timestamp is not None

    def is_expired(self, life_in_secs):
        if self._timestamp is not None:
            return self._timestamp + life_in_secs < int(time.time())

        return False

    @property
    def tag(self):
        return self._tag

    @property
    def token(self):
        return self._token
