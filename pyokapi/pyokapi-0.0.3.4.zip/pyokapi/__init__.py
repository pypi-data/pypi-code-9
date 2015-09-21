import os
import threading

import logging
log = logging.getLogger(__name__)

_OKAPI_TEST = os.environ.get("OKAPI_TEST", True)
if _OKAPI_TEST:
    _OKAPI_SCHEME = 'http'
    _OKAPI_HOST = 'api.ok-api.cn'
else:
    _OKAPI_SCHEME = 'http'
    _OKAPI_HOST = 'api.okapi.pub'

if _OKAPI_SCHEME != 'https':
    os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "True")

_okapi_url_base = "%s://%s" % (_OKAPI_SCHEME, _OKAPI_HOST)   

log.debug("okapi base url: %s" % _okapi_url_base)

api = threading.local()

_inited = False
_user_name = None
_private_token = None
_service_name = None

def init(user_name, private_token, service_name = None):
    global _inited, _user_name, _private_token, _service_name
    _user_name = user_name
    _private_token = private_token
    _service_name = service_name
    _inited = True
    log.debug("init success with account: %s, default service: %s" % (_user_name, _service_name))
    return _inited
def is_inited():
    return _inited

def get_user_name():
    return _user_name

def get_default_service():
    return _service_name

from .client import ServiceClient

from . import server
