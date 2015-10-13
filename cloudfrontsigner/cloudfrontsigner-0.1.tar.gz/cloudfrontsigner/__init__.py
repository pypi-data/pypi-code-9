# -*- coding: utf-8 -*-

import base64
import collections
import json
import rsa
import time
from .compat import urlencode


__version__ = '0.1'


class TrimedJSONEncoder(json.JSONEncoder):
    item_separator = ','
    key_separator = ':'


class Signer(object):

    policy_context = {}

    def __init__(self, key_pair_id=None, key_path=None, key_format=None,
                 hash_method=None):
        assert key_pair_id
        assert key_path

        self.key_pair_id = key_pair_id
        with open(key_path, 'rb') as f:
            key_data = f.read()
        key_format = 'PEM' if key_format is None else key_format
        self.key = rsa.PrivateKey.load_pkcs1(key_data, key_format)
        self.hash_method = 'SHA-1' if hash_method is None else hash_method

    def sign(self, url, **kwargs):
        url, kwargs = self.prepare(url, kwargs)
        policy = self.gen_policy(url, **kwargs)
        #print(policy)
        polbytes = self.jsonify(policy)
        #print(polbytes)
        signature = rsa.sign(polbytes, self.key, self.hash_method)
        # print(signature)
        sigstr = self.b64encode(signature)
        # print(sigstr)
        params = self.gen_params(url, sigstr, **kwargs)
        parastr = urlencode(params, safe='~')
        # print(parastr)
        signed = '?'.join([url, parastr])
        # print(signed)
        return signed

    def prepare(self, url, kw):
        return url, kw

    def gen_policy(self, url, **kwargs):
        pass

    def gen_params(self, url, signature, **kwargs):
        return {'Key-Pair-Id': self.key_pair_id, 'Signature': signature,}

    @staticmethod
    def b64encode(s):
        return base64.b64encode(s) \
            .decode('ascii') \
            .replace('+', '-') \
            .replace('=', '_') \
            .replace('/', '~')

    @staticmethod
    def jsonify(v):
        s = json.dumps(v, cls=TrimedJSONEncoder)
        b = s.encode('utf-8')
        return b


class CannedPolicySigner(Signer):

    def __init__(self, expire_seconds=None, **kwargs):
        super(CannedPolicySigner, self).__init__(**kwargs)
        self.expire_seconds = 600 if expire_seconds is None else expire_seconds

    def prepare(self, url, kwargs):
        url, kwargs = super(CannedPolicySigner, self).prepare(url, kwargs)
        kwargs['expired_at'] = int(time.time() + self.expire_seconds)
        return url, kwargs

    def gen_policy(self, url, **kwargs):
        expired_at = kwargs.get('expired_at', 0)
        stmt = collections.OrderedDict()
        stmt['Resource'] = url
        stmt['Condition'] = {'DateLessThan': {'AWS:EpochTime': expired_at}}
        policy = {'Statement': [stmt]}
        return policy

    def gen_params(self, url, signature, **kwargs):
        params = super(CannedPolicySigner, self).gen_params(
            url, signature, **kwargs
        )
        params['Expires'] = kwargs.get('expired_at', 0)
        return params
