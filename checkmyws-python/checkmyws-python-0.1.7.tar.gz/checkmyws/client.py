# -*- coding: utf-8 -*-
"""
python client for www.checkmy.ws
"""
import sys
PY26 = sys.version_info[0] == 2 and sys.version_info[1] == 6

import logging
import requests
import json

from checkmyws.exception import CheckmywsError

if PY26:
    requests.packages.urllib3.disable_warnings()

else:
    logging.captureWarnings(True)

BASE_URL = "https://api.checkmy.ws/api"


class CheckmywsClient(object):

    def __init__(self, proxy=None, verify=True):
        self.logger = logging.getLogger("CheckmywsClient")
        self.logger.debug("Initialize")

        self.session = requests.Session()
        self.proxies = None
        self.verify = verify

        if PY26:
            self.verify = False

        if proxy is not None:
            self.proxies = {
                "http": proxy,
                "https": proxy
            }

    def request(self, path, method="GET", params=None, data=None,
                status_code=200):
            """
            Make a http request to API
            """
            url = "{0}{1}".format(BASE_URL, path)

            if params is None:
                params = {}

            if data is not None and not isinstance(data, str):
                data = json.dumps(data)

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                verify=self.verify,
                proxies=self.proxies
            )

            if response.status_code == status_code:
                return response
            else:
                raise CheckmywsError(response)

    def status(self, check_id):
        path = "/status/{0}".format(check_id)
        response = self.request(path=path, method="GET")

        return response.json()
