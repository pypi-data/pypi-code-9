# -*- coding: UTF-8 -*-
__author__ = "d01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2015, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2015-07-30"
# Created: 2015-07-30 04:44

import requests

api_url = "https://api.airgramapp.com/1/"


class Airgram(object):
    """ Wrapper class to make calls to http://www.airgramapp.com/api """


    def __init__(self, key=None, secret=None, verify_certs=True):
        """
        Initialize object

        :param key: Service key
        :type key: None | str
        :param secret: Service secret
        :type secret: None | str
        :param verify_certs: Verify the certificates when making a request
        :type verify_certs: 
        :return:
        :rtype:
        """
        self.session = requests.Session()
        if key is not None:
            self.session.auth = (key, secret)
        self.verify_certs = verify_certs


    def send_as_guest(self, email, msg, url=None):
        """
        Sends an Airgram message to a user who already has the Airgram app

        :param email: Email address of the Airgram account you want to message
        :type email: str
        :param msg: Text of the message
        :type msg: str
        :param url: URL to open when the recipient opens the message
            (default: None) if None -> no url
        :type url: None | str
        :return: Response from server
        :rtype: dict
        """
        return self._request("send_as_guest", email, msg, url)


    def subscribe(self, email):
        """
        Subscribes an email address to the authenticated Airgram service

        :param email: Email address to subscribe
        :type email: str
        :return: Response from server
        :rtype: dict
        """
        return self._request("subscrube", email)


    def send(self, email, msg, url=None):
        """
        Sends an Airgram message to a subscriber of the
        authenticated Airgram service

        :param email: Email address of the subscriber you want to message
        :type email: str
        :param msg: Text of the message
        :type msg: str
        :param url: URL to open when the recipient opens the message
            (default: None) if None -> no url
        :type url: None | str
        :return: Response from server
        :rtype: dict
        """
        return self._request("send", email, msg, url)


    def broadcast(self, msg, url=None):
        """
        Sends an Airgram message to all subscribers of the
        authenticated Airgram service

        :param msg: Text of the message
        :type msg: str
        :param url: URL to open when the recipient opens the message
            (default: None) if None -> no url
        :type url: None | str
        :return: Response from server
        :rtype: dict
        """
        return self._request("send", None, msg, url)


    def _request(self, method, email=None, msg=None, url=None):
        """
        Make request to airgram api

        :param method: Which method to invoke on the api
        :type method: None | str
        :param email: email parameter
        :type email: None | str
        :param msg: msg parameter
        :type msg: None | str
        :param url: url parameter
        :type url: None | str
        :return: Response from server
        :rtype: dict
        """
        parameter = {}
        if email:
            parameter['email'] = email
        if msg:
            parameter['msg'] = msg
        if url:
            parameter['url'] = url
        resp = self.session.get(
            api_url + method, params=parameter, verify=self.verify_certs
        )
        return resp.json()