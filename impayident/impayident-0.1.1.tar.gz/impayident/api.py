# -*- coding: utf-8 -*-

from collections import namedtuple
import hashlib
import requests
from .exc import HttpException, ApiException

from . import lib
from . import env

from .const import *


class Request(object):
    URL = ''
    KEYS = []

    Response = None

    def __init__(self, **kwargs):
        self.env = kwargs.get('env', env.default)
        self.lib = lib.Library(self.env)
        kwargs = self._refine_init_args(kwargs)
        self.data = []
        for i, key in enumerate(self.KEYS):
            if key not in kwargs:
                raise TypeError(
                    u'key #{} {} is expected but not found'.format(i, key))
            datum = kwargs[key]
            setattr(self, key, datum)
            self.data.append(datum)

    def _refine_init_args(self, kwargs):
        raise NotImplementedError

    def __getitem__(self, index):
        try:
            intindex = int(index) - 1
            if intindex == len(self.KEYS) + 1:
                return self.CERTIFY
            return self.data[intindex]
        finally:
            return getattr(self, index)

    @property
    def string_data(self):
        return [u'{}'.format(datum) for datum in self.data]

    @property
    def CERTIFY(self):
        raw_string = u'/'.join(self.string_data)
        fucked = raw_string.encode('euc-kr')
        return hashlib.sha256(fucked).hexdigest()

    @property
    def cert_data(self):
        raw_string = '/'.join(self.string_data + [self.CERTIFY])
        fucked = raw_string.encode('euc-kr')
        return fucked

    def send(self):
        assert self.URL.startswith('http')
        encrypted = self.lib.encrypt_01(self.cert_data)
        response = requests.get(self.URL, {'cert_data': encrypted})
        if response.status_code != 200:
            raise HttpException(
                code=response.status_code, text=response.text,
                response=response)
        decrypted = self.lib.decrypt_01(response.text)
        unfucked = decrypted.decode('euc-kr')
        response = self.Response(*unfucked.split('/'))
        if response.RESULT != '0000':
            raise ApiException(
                code=response.RESULT, message=response.RESULTMSG,
                response=response)
        return response


CertResponse = namedtuple('CertResponse', [
    'CPCODE', 'CPORDERNO', 'CERTTYPE', 'TELECOM', 'NAME', 'PHONENO',
    'BIRTHDAY', 'SEX', 'KOREANFLAG', 'ACCESSFLAG', 'CERTTXID', 'RESULT',
    'SUBRET', 'RESULTMSG', 'CERTIFY'])


class CertRequest(Request):
    URL = 'https://cert.impay.co.kr/api/cert.do'
    KEYS = [
        'CPCODE', 'CPORDERNO', 'CERTTYPE', 'TELECOM', 'NAME', 'PHONENO',
        'BIRTHDAY', 'SEX', 'KOREANFLAG', 'ACCESSFLAG']
    Response = CertResponse

    def _refine_init_args(self, kwargs):
        if 'CPCODE' not in kwargs:
            kwargs['CPCODE'] = self.env.CPCODE
        if 'CERTTYPE' not in kwargs:
            kwargs['CERTTYPE'] = self.env.CERTTYPE
        if kwargs['TELECOM'] not in TELECOMS:
            raise ValueError
        if kwargs['SEX'] not in [MALE, FEMALE]:
            raise ValueError
        flags = kwargs['ACCESSFLAG']
        if isinstance(flags, list) or isinstance(flags, tuple):
            kwargs['ACCESSFLAG'] = ''.join(flags)
        if kwargs['KOREANFLAG'] not in [YES, NO]:
            raise ValueError
        for flag in kwargs['ACCESSFLAG']:
            if flag not in [YES, NO]:
                raise ValueError
        return kwargs


BillResponse = namedtuple('BillResponse', [
    'CPCODE', 'CPORDERNO', 'CERTTXID', 'PASSWORD', 'CI', 'DI', 'RESULT',
    'SUBRET', 'RESULTMSG', 'CERTIFY'])


class BillRequest(Request):
    URL = 'https://cert.impay.co.kr/api/bill.do'
    KEYS = ['CPCODE', 'CPORDERNO', 'CERTTXID', 'PASSWORD']

    Response = BillResponse

    def _refine_init_args(self, kwargs):
        if 'CPCODE' not in kwargs:
            kwargs['CPCODE'] = self.env.CPCODE
        if len(kwargs['PASSWORD']) != 6:
            raise ValueError
        return kwargs


SmsResponse = namedtuple('BillResponse', [
    'CPCODE', 'CPORDERNO', 'CERTTXID', 'RESULT', 'SUBRET', 'RESULTMSG',
    'CERTIFY'])


class SmsRequest(Request):
    URL = 'https://cert.impay.co.kr/api/sms.do'

    KEYS = ['CPCODE', 'CPORDERNO', 'CERTTXID']

    Response = SmsResponse

    def _refine_init_args(self, kwargs):
        if 'CPCODE' not in kwargs:
            kwargs['CPCODE'] = self.env.CPCODE
        return kwargs


def cert(**kwargs):
    """고객 식별 인증 요청"""
    return CertRequest(**kwargs).send()


def bill(**kwargs):
    """인증번호 인증 요청"""
    return BillRequest(**kwargs).send()


def sms(**kwargs):
    """SMS 재발송 요청"""
    return SmsRequest(**kwargs).send()
