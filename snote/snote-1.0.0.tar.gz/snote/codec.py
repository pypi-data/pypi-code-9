# coding:utf-8

import base64
import hashlib
import hmac
import json
import time
import uuid
from .snote import Snote


class Codec(object):
    def __init__(self,
                 key,
                 hash_f=hashlib.sha256,
                 encode_f=json.dumps,
                 decode_f=json.loads,
                 tag_f=lambda: uuid.uuid4().hex):
        self._key = self._to_bytes(key)
        self._hash_f = hash_f
        self._encode_f = encode_f
        self._decode_f = decode_f
        self._tag_f = tag_f

    def encode(self, obj):
        data = obj, int(time.time()), self._tag_f()
        encoded = self._encode_f(data)
        token = self._sign(self._to_bytes(encoded))
        return Snote(data, token)

    def decode(self, token):
        encoded = self._unsign(self._to_bytes(token))
        if encoded is not None:
            data = self._decode_f(self._to_unicode(encoded))
            return Snote(data, token)

        else:
            return Snote((None, None, None), token)

    def _to_unicode(self, s):
        return s.decode() if isinstance(s, bytes) else s

    def _to_bytes(self, s):
        return s if isinstance(s, bytes) else s.encode()

    def _sign(self, b):
        sig = self._create_signature(b)
        return self._b64encode(b) + b'.' + self._b64encode(sig)

    def _unsign(self, b):
        ls = b.split(b'.')
        if len(ls) == 2:
            body, sig = self._b64decode(ls[0]), self._b64decode(ls[1])
            if self._create_signature(body) == sig:
                return body

        return None

    def _create_signature(self, b):
        return hmac.new(self._key, b, self._hash_f).digest()

    def _b64encode(self, b):
        return base64.urlsafe_b64encode(b).rstrip(b'=')

    def _b64decode(self, b):
        return base64.urlsafe_b64decode(b + b'='*((4 - len(b) % 4) % 4))
