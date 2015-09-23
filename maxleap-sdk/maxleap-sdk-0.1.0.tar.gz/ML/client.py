# coding: utf-8

import json

import requests
requests.packages.urllib3.disable_warnings()

import ML
from ML import utils

__author__ = 'czhou <czhou@ilegendsoft.com>'


APP_ID = None
CLIENT_KEY = None
MASTER_KEY = None
BY_HOOK = None

CN_BASE_URL = 'https://api.leap.as'
CN_BASE_URL = 'https://api.leap.as'

SERVER_VERSION = '2.0'
SDK_VERSION = '1.0.0'
BASE_URL = CN_BASE_URL + '/' + SERVER_VERSION
TIMEOUT_SECONDS = 15

headers = None

def by_hook(flag):
    """
    :type flag: bool
    :param flag: 当请求从CloudCode发起的时候，标志为True
    """
    global BY_HOOK
    BY_HOOK = flag


def init(app_id, client_key=None, master_key=None):
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
    global APP_ID, CLIENT_KEY, MASTER_KEY
    APP_ID = app_id
    CLIENT_KEY = client_key
    MASTER_KEY = master_key


def need_init(func):
    def new_func(*args, **kwargs):
        if APP_ID is None:
            raise RuntimeError('MaxLeap SDK must be initialized')

        global headers
        if not headers:
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
            }
        headers['Content-Type'] = 'application/json'
        headers['X-LAS-AppId'] = APP_ID
        headers['User-Agent'] = 'MaxLeap Code Python-{0}SDK'.format(ML.__version__)
        if MASTER_KEY:
            headers['X-LAS-MasterKey'] = MASTER_KEY
        else:
            headers['X-LAS-APIKey'] = CLIENT_KEY

        if BY_HOOK:
            headers['X-ZCloud-Request-From-Cloudcode'] = "true"
        else:
            headers['X-ZCloud-Request-From-Cloudcode'] = "false"
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
def get(url, params):
    for k, v in params.iteritems():
        if isinstance(v, dict):
            params[k] = json.dumps(v)
    response = requests.get(BASE_URL + url, headers=headers, params=params, timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('create')
def post(url, params):
    response = requests.post(BASE_URL + url, headers=headers, data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('update')
def put(url, params):
    response = requests.put(BASE_URL + url, headers=headers, data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response

@need_init
@check_error
@handler_hook('delete')
def delete(url, params=None):
    response = requests.delete(BASE_URL + url, headers=headers, data=json.dumps(params), timeout=TIMEOUT_SECONDS, verify=False)
    return response
