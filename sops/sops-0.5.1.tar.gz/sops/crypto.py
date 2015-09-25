#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contributor: Julien Vehent <jvehent@mozilla.com> [:ulfr]
# Contributor: Daniel Thornton <daniel@relud.com>
# Contributor: Alexis Metaireau <alexis@mozilla.com> [:alexis]
# Contributor: Rémy Hubscher <natim@mozilla.com> [:natim]

import os
from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms


def encrypt(value, key, stash=None):
    """Return an encrypted string of the value provided."""
    value = value.encode('utf-8')
    # if we have a stash, and the value of cleartext has not changed,
    # attempt to take the IV and AAD value from the stash.
    # if the stash has no existing value, or the cleartext has changed,
    # generate new IV and AAD.
    if stash and stash['cleartext'] == value:
        iv = stash['iv']
        aad = stash['aad']
    else:
        iv = os.urandom(32)
        aad = os.urandom(32)
    encryptor = Cipher(algorithms.AES(key),
                       modes.GCM(iv),
                       default_backend()).encryptor()
    encryptor.authenticate_additional_data(aad)
    enc_value = encryptor.update(value) + encryptor.finalize()
    return "ENC[AES256_GCM,data:{value},iv:{iv},aad:{aad}," \
           "tag:{tag}]".format(value=b64encode(enc_value).decode('utf-8'),
                               iv=b64encode(iv).decode('utf-8'),
                               aad=b64encode(aad).decode('utf-8'),
                               tag=b64encode(encryptor.tag).decode('utf-8'))


def decrypt(value, key, stash=None):
    """Return a decrypted value."""
    # operate on bytes, but return a string
    value = value.encode('utf-8')
    # extract fields using a regex
    res = re.match(b'^ENC\[AES256_GCM,data:(.+),iv:(.+),aad:(.+),tag:(.+)\]$',
                   value)
    # if the value isn't in encrypted form, return it as is
    if res is None:
        return value
    enc_value = b64decode(res.group(1))
    iv = b64decode(res.group(2))
    aad = b64decode(res.group(3))
    tag = b64decode(res.group(4))
    decryptor = Cipher(algorithms.AES(key),
                       modes.GCM(iv, tag),
                       default_backend()
                       ).decryptor()
    decryptor.authenticate_additional_data(aad)
    cleartext = decryptor.update(enc_value) + decryptor.finalize()
    if stash:
        # save the values for later if we need to reencrypt
        stash['iv'] = iv
        stash['aad'] = aad
        stash['cleartext'] = cleartext
    return cleartext.decode('utf-8')
