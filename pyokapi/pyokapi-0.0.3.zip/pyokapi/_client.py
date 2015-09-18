# -*- coding:utf-8 -*-
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

import logging
log = logging.getLogger(__name__)

from pyokapi import _okapi_url_base, is_inited, get_user_name, get_default_service

class ServiceClient(OAuth2Session):

    def __init__(self, name = None, owner = None, version = '1', client_id=None, auto_refresh_url=None,
            auto_refresh_kwargs=None, scope=None, token=None,
            state=None, token_updater=None, **kwargs):
        
        self.name = name if name else get_default_service()
        self.owner = owner if owner else get_user_name()
        self.version = version
        
        if not client_id:
            client_id = self.name
        client = BackendApplicationClient(client_id, token = token)
        super(ServiceClient, self).__init__(client_id=client_id, client = client, auto_refresh_url=auto_refresh_url,
            auto_refresh_kwargs=auto_refresh_kwargs, scope=scope, token=token,
            state=state, token_updater=token_updater, **kwargs)


    def request(self, method, url, ignore_auth = False, **kwargs):
        
        if not is_inited():
            raise Exception("pyokap client must init first, please call init first")

        if not url.startswith('/'):
            url = "/%s" % url
        url = "%s/%s/%s/%s%s" % (_okapi_url_base, self.owner, self.name, self.version, url)
        return super(ServiceClient, self).request(method, url, **kwargs)



