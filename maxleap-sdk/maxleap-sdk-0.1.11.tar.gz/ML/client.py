# coding: utf-8

import json
import copy

import requests
requests.packages.urllib3.disable_warnings()

import ML
from ML import utils

__author__ = 'czhou <czhou@ilegendsoft.com>'

APP_ID = None
BY_HOOK = None

US_BASE_URL = 'https://api.leap.as'
CN_BASE_URL = 'https://api.leapcloud.cn'
UAT_BASE_URL = 'http://apiuat.leap.as'
DEV_BASE_URL = 'http://apidev.leap.as'

SERVER_VERSION = '2.0'
SDK_VERSION = '1.0.0'
BASE_URL = US_BASE_URL + '/' + SERVER_VERSION
TIMEOUT_SECONDS = 15

MASTER_USER_PRINCIPAL = None

def get_master_principal():
    return MASTER_USER_PRINCIPAL

class UserPrincipal(object):
    """docstring for UserPrincipal"""
    def __init__(self, app_id, client_key=None, master_key=None, session_token=None):
        super(UserPrincipal, self).__init__()
        self.app_id = app_id
        self.client_key = client_key
        self.master_key = master_key
        self.session_token = session_token
        self.headers = {
            'Content-Type':'application/json;charset=utf-8',
            'User-Agent':'MaxLeap Code Python-{0}SDK'.format(ML.__version__)
        }
        self.validate()

    def validate(self):
        if not any([self.client_key, self.master_key, self.session_token]):
            raise RuntimeError('client_key or master_key or session_token must be specified')
        if not self.app_id:
            raise RuntimeError('app_id must be specified')

    def gen_headers(self):
        self.headers['X-LAS-AppId'] = self.app_id
        if self.master_key:
            self.headers['X-LAS-MasterKey'] = self.master_key
        elif self.client_key:
            self.headers['X-LAS-APIKey'] = self.client_key
        elif self.session_token:
            self.headers['X-LAS-Session-Token'] = self.session_token
        return self.headers

    def injection(self,headers):
        self.headers.update(headers)


def change_region(region='us'):
    global BASE_URL
    if region == 'us':
        BASE_URL = US_BASE_URL + '/' + SERVER_VERSION
    if region == 'cn':
        BASE_URL = CN_BASE_URL + '/' + SERVER_VERSION
    if region == 'uat':
        BASE_URL = UAT_BASE_URL + '/' + SERVER_VERSION
    if region == 'dev':
        BASE_URL = DEV_BASE_URL + '/' + SERVER_VERSION

def by_hook(flag):
    """
    :type flag: bool
    :param flag: 当请求从cloudCode发起的时候，标志为True
    """
    global BY_HOOK
    BY_HOOK = flag


def init(app_id, client_key=None, master_key=None, region='us'):
    """初始化 MaxLeap 的 AppId / REST API Key / MasterKey

    :type app_id: basestring
    :param app_id: 应用的 Application ID
    :type client_key: None or basestring
    :param client_key: 应用的 REST API Key
    :type master_key: None or basestring
    :param master_key: 应用的 Master Key
    """
    if (not client_key) and (not master_key):
        raise RuntimeError('client_key or master_key must be specified')
    global MASTER_USER_PRINCIPAL, APP_ID
    APP_ID = app_id
    MASTER_USER_PRINCIPAL = UserPrincipal(app_id, client_key=client_key, master_key=master_key)
    change_region(region)


def need_init(func):
    def new_func(*args, **kwargs):
        if MASTER_USER_PRINCIPAL is None:
            raise RuntimeError('MaxLeap SDK must be initialized')
        if not kwargs.get('principal'):
            kwargs['principal'] = ML.get_principal() or copy.deepcopy(MASTER_USER_PRINCIPAL)
        if BY_HOOK:
            kwargs['principal'].injection({'X-ZCloud-Request-From-Cloudcode':'true'})
        return func(*args, **kwargs)
    return new_func


def check_error(func):
    def new_func(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.headers.get('Content-Type') == 'text/html':
            raise ML.MaxLeapError(-1, 'Bad Request')
        content = utils.response_to_json(response)
        if 'errorCode' in content:
            raise ML.MaxLeapError(content.get('errorCode', 1), content.get('errorMessage', 'Unknown Error'))
        return response
    return new_func

def handler_hook(method):
    def _deco(func):
        def new_func(*args, **kwargs):
            global BY_HOOK
            if ML.PRO or BY_HOOK:
                return func(*args, **kwargs)
            else:
                path = args[0]
                url_parts = path.split('/')
                obj_id = None
                class_name = None
                if len(url_parts) == 3:
                    class_name = url_parts[2]
                elif len(url_parts) == 4:
                    class_name = url_parts[2]
                    obj_id = url_parts[3]
                else:
                    return func(*args, **kwargs)

                if class_name not in ML.Server._hook_classes:
                    return func(*args, **kwargs)

                if method == "create":
                    BY_HOOK = True
                    res = ML.Server._handel_hook(class_name, method, args[1])
                    BY_HOOK = False
                    return res

                if method == "update":
                    BY_HOOK = True
                    res = ML.Server._handel_hook(class_name, method, {"update": args[1], "objectId": obj_id})
                    BY_HOOK = False
                    return res

                if method == "delete":
                    BY_HOOK = True
                    res = ML.Server._handel_hook(class_name, method, {"objectId": obj_id})
                    BY_HOOK = False
                    return res

                return func(*args, **kwargs)
        return new_func
    return _deco


@need_init
@check_error
def get(url, params, principal=None):
    for k, v in params.iteritems():
        if isinstance(v, dict):
            params[k] = json.dumps(v)
    response = requests.get(BASE_URL + url, headers=principal.gen_headers(), params=params, timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('create')
def post(url, params, principal=None):
    response = requests.post(BASE_URL + url, headers=principal.gen_headers(), data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('update')
def put(url, params, principal=None):
    response = requests.put(BASE_URL + url, headers=principal.gen_headers(), data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('delete')
def delete(url, params=None, principal=None):
    response = requests.delete(BASE_URL + url, headers=principal.gen_headers(), data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response
