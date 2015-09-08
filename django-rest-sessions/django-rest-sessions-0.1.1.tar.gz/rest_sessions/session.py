import json

import requests
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase


class SessionStore(SessionBase):

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self.original_session = {}

    def session_url(self, action, session_key):
        if not hasattr(settings, 'SESSION_URL'):
            raise Exception('SESSION_URL is not defined in the settings')
        if not hasattr(settings, 'SESSION_APP'):
            raise Exception('SESSION_APP is not defined in the settings')
        url = settings.SESSION_URL + '/' + settings.SESSION_APP
        url += '/' + action + '/' + session_key
        return url

    def load(self):
        session_data = {}
        if self.session_key:
            url = self.session_url('get', self.session_key)
            r = requests.get(url)
            response = r.json()
            if 'd' in response:
                session_data = response['d']
                self.original_session = response['d']
        return session_data

    def exists(self, session_key):
        url = self.session_url('get', session_key)
        r = requests.get(url)
        return r.json() != {}

    def save(self, must_create=False):
        if self.session_key is None:
            return

        session = self._get_session(no_load=False)
        payload = {}

        for key in session.keys():
            if key not in self.original_session or \
                self.original_session[key] != session[key]:
                    payload[key] = session[key]

        if payload:
            url = self.session_url('set',self.session_key)
            r = requests.post(url, json=payload)

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        url = self.session_url('kill', session_key)
        r = requests.delete(url)

    def create(self):
        pass

    @classmethod
    def clear_expired(cls):
        pass
