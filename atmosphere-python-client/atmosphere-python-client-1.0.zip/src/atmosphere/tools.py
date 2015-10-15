import httplib
import inspect
import simplejson
import socket
import logging

from atmosphere import config


__author__ = 'paoolo'

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'

__console_handler = logging.StreamHandler()
__console_handler.setLevel(logging.INFO)

__logger = logging.getLogger('air_python')
__logger.addHandler(__console_handler)


def _get_content(api_url, method, api_prefix, url, body, headers, https=False):
    try:
        if https:
            connection = httplib.HTTPSConnection(api_url)
        else:
            connection = httplib.HTTPConnection(api_url)

        connection.request(method, api_prefix + url, body, headers=headers)

        response = connection.getresponse()
        # TODO: check code status
        if not 200 <= response.status < 300:
            raise httplib.HTTPException('Response code is %d' % response.status)

        content = response.read()

        response.close()
        connection.close()

        return content

    except httplib.HTTPException as h_exp:
        __logger.warning('HTTP exception: %s' % str(h_exp))
        raise h_exp

    except socket.error as s_exp:
        __logger.error('Socket exception: %s' % str(s_exp))
        raise s_exp


def _check_and_set_headers(headers, keys_values):
    for key, value in keys_values.items():
        _check_and_set_header(headers, key, value)


def _check_and_set_header(headers, key, value):
    if not key in headers and value is not None:
        headers[key] = value


def _parse_as_json(content):
    try:
        return simplejson.loads(content)
    except simplejson.JSONDecodeError as j_exp:
        __logger.error('JSON exception: %s' % str(j_exp))
        return {}


def get_prefix():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])

    try:
        return mod.PREFIX
    except AttributeError as a_exp:
        __logger.warning('No PREFIX defined in module %s' % str(mod.__name__))
        raise a_exp


def _create_req(method=HTTP_GET, url='', body=None, headers=None):
    if not headers:
        headers = {}

    _check_and_set_headers(headers, {'PRIVATE-TOKEN': config.API_PRIVATE_TOKEN,
                                     'MI-TICKET': config.API_MI_TICKET})

    content = _get_content(config.API_URL, method, config.API_PREFIX, url, body, headers, (config.HTTPS == 'True'))
    data = _parse_as_json(content)

    return data


def create_req(method=HTTP_GET, url='', body=None, headers=None):
    url = get_prefix() + url
    return _create_req(method, url, body, headers)


def create_req_json_body(method=HTTP_GET, url='', body=None, headers=None):
    if not headers:
        headers = {}

    body = simplejson.dumps(body)

    _check_and_set_headers(headers, {'Content-Length': len(body),
                                     'Content-Type': 'application/json'})

    url = get_prefix() + url
    return _create_req(method, url, body, headers)


def get_data(data):
    return dict(filter(lambda val: val[1] is not None, data.items()))