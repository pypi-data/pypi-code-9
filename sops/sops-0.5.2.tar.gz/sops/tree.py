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


def load_tree(path, filetype):
    """Load the tree.

    Read data from `path` using format defined by `filetype`.
    Return a dictionary with the data.

    """
    tree = dict()
    with open(path, "rt") as fd:
        if filetype == 'yaml':
            tree = ruamel.yaml.load(fd, ruamel.yaml.RoundTripLoader)
        elif filetype == 'json':
            tree = json.load(fd)
        else:
            for line in fd:
                if line.startswith('SOPS='):
                    tree['sops'] = json.loads(
                        line.rstrip('\n').split('=', 1)[1])
                else:
                    if 'data' not in tree:
                        tree['data'] = str()
                    tree['data'] += line
    return tree


def verify_or_create_sops_branch(tree):
    """Verify or create the sops branch in the tree.

    If the current tree doesn't have a sops branch with either kms or pgp
    information, create it using the content of the global variables and
    indicate that an encryption is needed when returning.

    """
    if 'sops' not in tree:
        tree['sops'] = dict()
        tree['sops']['attention'] = 'This section contains key material' + \
            ' that should only be modified with extra care. See `sops -h`.'
    if 'kms' in tree['sops'] and isinstance(tree['sops']['kms'], list):
        # check that we have at least one ARN to work with
        for entry in tree['sops']['kms']:
            if 'arn' in entry and entry['arn'] != "":
                return tree, False
    # if we're here, no arn was found
    if 'pgp' in tree['sops'] and isinstance(tree['sops']['pgp'], list):
        # check that we have at least one fingerprint to work with
        for entry in tree['sops']['pgp']:
            if 'fp' in entry and entry['fp'] != "":
                return tree, False
    # if we're here, no fingerprint was found either
    has_at_least_one_method = False
    if SOPS_KMS_ARN != "":
        tree['sops']['kms'] = list()
        for arn in SOPS_KMS_ARN.split(','):
            entry = {"arn": arn.replace(" ", "")}
            tree['sops']['kms'].append(entry)
            has_at_least_one_method = True
    if SOPS_PGP_FP != "":
        tree['sops']['pgp'] = list()
        for fp in SOPS_PGP_FP.split(','):
            entry = {"fp": fp.replace(" ", "")}
            tree['sops']['pgp'].append(entry)
            has_at_least_one_method = True
    if not has_at_least_one_method:
        panic("Error: No KMS ARN or PGP Fingerprint found to encrypt the data "
              "key, read the help (-h) for more information.", 111)
    # return True to indicate an encryption key needs to be created
    return tree, True


def walk_and_decrypt(branch, key, stash=None):
    """Walk the branch recursively and decrypt leaves."""
    for k, v in branch.items():
        if k == 'sops':
            continue    # everything under the `sops` key stays in clear
        nstash = dict()
        if stash:
            stash[k] = {'has_stash': True}
            nstash = stash[k]
        if isinstance(v, dict):
            branch[k] = walk_and_decrypt(v, key, nstash)
        elif isinstance(v, list):
            branch[k] = walk_list_and_decrypt(v, key, nstash)
        elif isinstance(v, ruamel.yaml.scalarstring.PreservedScalarString):
            ev = decrypt(v, key, nstash)
            branch[k] = ruamel.yaml.scalarstring.PreservedScalarString(ev)
        else:
            branch[k] = decrypt(v, key, nstash)
    return branch


def walk_list_and_decrypt(branch, key, stash=None):
    """Walk a list contained in a branch and decrypts its values."""
    nstash = dict()
    kl = []
    for i, v in enumerate(list(branch)):
        if stash and i in stash:
            nstash = stash[i]
        if isinstance(v, dict):
            kl.append(walk_and_decrypt(v, key, nstash))
        elif isinstance(v, list):
            kl.append(walk_list_and_decrypt(v, key, nstash))
        else:
            kl.append(decrypt(v, key, nstash))
    return kl


def walk_and_encrypt(branch, key, stash=None):
    """Walk the branch recursively and encrypts its leaves."""
    for k, v in branch.items():
        if k == 'sops':
            continue    # everything under the `sops` key stays in clear
        nstash = dict()
        if stash and k in stash:
            nstash = stash[k]
        if isinstance(v, dict):
            # recursively walk the tree
            branch[k] = walk_and_encrypt(v, key, nstash)
        elif isinstance(v, list):
            branch[k] = walk_list_and_encrypt(v, key, nstash)
        elif isinstance(v, ruamel.yaml.scalarstring.PreservedScalarString):
            ev = encrypt(v, key, nstash)
            branch[k] = ruamel.yaml.scalarstring.PreservedScalarString(ev)
        else:
            branch[k] = encrypt(v, key, nstash)
    return branch


def walk_list_and_encrypt(branch, key, stash=None):
    """Walk a list contained in a branch and encrypts its values."""
    nstash = dict()
    kl = []
    for i, v in enumerate(list(branch)):
        if stash and i in stash:
            nstash = stash[i]
        if isinstance(v, dict):
            kl.append(walk_and_encrypt(v, key, nstash))
        elif isinstance(v, list):
            kl.append(walk_list_and_encrypt(v, key, nstash))
        else:
            kl.append(encrypt(v, key, nstash))
    return kl
