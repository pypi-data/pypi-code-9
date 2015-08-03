# -*- coding:utf-8 -*-
VERSION = '0.0.2'

import requests
import xmltodict
import dicttoxml


class APIResponse(object):

    def __init__(self, status, description, data=None):
        self.status = status
        self.description = description
        self.data = data

    def __str__(self):
        return '%s %s\n %s' % (self.status, self.description, self.data)


def post(url, body):
    rsp = requests.post(url, data=body,
                        headers={'content_type': 'application/xml'})
    if rsp.status_code != 200:
        return APIResponse(-100, 'unexcpected http status %s' %
                           rsp.status_code)
    try:
        return parse_response(rsp.text)
    except:
        return APIResponse(-101, 'unexpected error:\n %s' % rsp.text)


def parse_response(ct):
    content = xmltodict.parse(ct)
    content = content.items()[0][1]
    common = content['CommonResponse']
    status = common['Status']
    description = common['Description']

    del content['CommonResponse']
    return APIResponse(status, description=description, data=content)


def prepare_request(request, parameters):
    """
    把数据转换成为xml
    @parameters 是一个字典，字典嵌套字典。
    """
    return dicttoxml.dicttoxml(parameters, attr_type=False,
                               custom_root=request, fold_list=False)


class Dytranscoder(object):

    def __init__(self, host):
        self.host = host

    def send_request(self, request, data):
        rsp = post(self.host + '/LeoVideoAPI/service/' + request,
                   prepare_request(
                       request[0].upper() + request[1:] + 'Request', data))
        return rsp

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return super(Dytranscoder, self).__getattr__(attr)

        def wrap(**kwargs):
            data = dict(**kwargs)
            return self.send_request(attr, data)
        return wrap
