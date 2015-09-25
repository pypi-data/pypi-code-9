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

from __future__ import print_function, unicode_literals
import subprocess

import ruamel.yaml


def get_key_from_pgp(tree):
    """Retreive the key from the PGP tree leave."""
    try:
        pgp_tree = tree['sops']['pgp']
    except KeyError:
        return None
    i = -1
    for entry in pgp_tree:
        i += 1
        try:
            enc = entry['enc']
        except KeyError:
            continue
        try:
            p = subprocess.Popen(['gpg', '-d'], stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            key = p.communicate(input=enc)[0]
        except Exception as e:
            print("PGP decryption failed in entry %s with error: %s" %
                  (i, e), file=sys.stderr)
            continue
        return key
    return None


def encrypt_key_with_pgp(key, tree):
    """Encrypt the key using the PGP key."""
    try:
        isinstance(tree['sops']['pgp'], list)
    except KeyError:
        return tree
    i = -1
    for entry in tree['sops']['pgp']:
        i += 1
        if 'fp' not in entry or entry['fp'] == "":
            print("PGP fingerprint not found, skipping entry %d" % i,
                  file=sys.stderr)
            continue
        fp = entry['fp']
        try:
            p = subprocess.Popen(['gpg', '--no-default-recipient', '--yes',
                                  '--encrypt', '-a', '-r', fp, '--trusted-key',
                                  fp[-16:], '--no-encrypt-to'],
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            enc = p.communicate(input=key)[0]
        except Exception as e:
            print("failed to encrypt key using pgp fp %s: %s, skipping it" %
                  (fp, e), file=sys.stderr)
            continue
        enc = enc.decode('utf-8')
        entry['enc'] = ruamel.yaml.scalarstring.PreservedScalarString(enc)
        entry['created_at'] = time.time()
        tree['sops']['pgp'][i] = entry
    return tree
