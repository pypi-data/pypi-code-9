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

import boto3


def get_key_from_kms(tree):
    """Get the key form the KMS tree leave."""
    try:
        kms_tree = tree['sops']['kms']
    except KeyError:
        return None
    i = -1
    for entry in kms_tree:
        i += 1
        try:
            enc = entry['enc']
        except KeyError:
            continue
        if 'arn' not in entry or entry['arn'] == "":
            print("KMS ARN not found, skipping entry %s" % i, file=sys.stderr)
            continue
        # extract the region from the ARN
        # arn:aws:kms:{REGION}:...
        res = re.match(r'^arn:aws:kms:(.+):([0-9]+):key/(.+)$',
                       entry['arn'])
        if res is None:
            print("Invalid ARN '%s' in entry %s" % (entry['arn'], i),
                  file=sys.stderr)
            continue
        try:
            region = res.group(1)
        except:
            print("Unable to find region from ARN '%s' in entry %s" %
                  (entry['arn'], i), file=sys.stderr)
            continue
        kms = boto3.client('kms', region_name=region)
        # use existing data key, ask kms to decrypt it
        try:
            kms_response = kms.decrypt(CiphertextBlob=b64decode(enc))
        except Exception as e:
            print("failed to decrypt key using kms: %s, skipping it" % e,
                  file=sys.stderr)
            continue
        return kms_response['Plaintext']
    return None


def encrypt_key_with_kms(key, tree):
    """Encrypt the key using the KMS."""
    try:
        isinstance(tree['sops']['kms'], list)
    except KeyError:
        return tree
    i = -1
    for entry in tree['sops']['kms']:
        i += 1
        if 'arn' not in entry or entry['arn'] == "":
            print("KMS ARN not found, skipping entry %d" % i, file=sys.stderr)
            continue
        arn = entry['arn']
        # extract the region from the ARN
        # arn:aws:kms:{REGION}:...
        res = re.match(r'^arn:aws:kms:(.+):([0-9]+):key/(.+)$',
                       arn)
        if res is None:
            print("Invalid ARN '%s' in entry %s" % (entry['arn'], i),
                  file=sys.stderr)
            continue
        try:
            region = res.group(1)
        except:
            print("Unable to find region from ARN '%s' in entry %s" %
                  (entry['arn'], i), file=sys.stderr)
            continue
        kms = boto3.client('kms', region_name=region)
        try:
            kms_response = kms.encrypt(KeyId=arn, Plaintext=key)
        except Exception as e:
            print("failed to encrypt key using kms arn %s: %s, skipping it" %
                  (arn, e), file=sys.stderr)
            continue
        entry['enc'] = b64encode(
            kms_response['CiphertextBlob']).decode('utf-8')
        entry['created_at'] = time.time()
        tree['sops']['kms'][i] = entry
    return tree
