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

from . import sops

from __future__ import print_function, unicode_literals
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from base64 import b64encode, b64decode
from textwrap import dedent

import ruamel.yaml

DESC = """
`sops` is an encryption manager and editor for files that contains secrets.

`sops` supports both AWS, KMS and PGP encryption:

    * To encrypt or decrypt a document with AWS KMS, specify the KMS ARN
      in the `-k` flag or in the ``SOPS_KMS_ARN`` environment variable.
      (you need valid credentials in ~/.aws/credentials)

    * To encrypt or decrypt using PGP, specify the PGP fingerprint in the
      `-g` flag or in the ``SOPS_PGP_FP`` environment variable.

Those flags are ignored if the document already stores encryption info.
Internally the KMS and PGP key IDs are stored in the document under
``sops.kms`` and ``sops.pgp``.

    YAML
        sops:
            kms:
            -   arn: "aws:kms:us-east-1:656532927350:key/305caadb"
            -   arn: "aws:kms:us-west-2:457153232612:key/f7da420e"
            pgp:
            -   fp: 85D77543B3D624B63CEA9E6DBC17301B491B3F21

    JSON
        {"sops": {
            "kms": [
                {"arn": "aws:kms:us-east-1:650:key/305caadb"},
                {"arn": "aws:kms:us-west-2:457153232612:key/f7da420e" }
            ],
            "pgp": [
                {"fp": 85D77543B3D624B63CEA9E6DBC17301B491B3F21}
            ]}
        }

    TEXT (JSON serialization of the `sops` object)
        SOPS={"sops":{"kms":[{"arn":"aws:kms:us-east-1:650:ke...}]}}

The ``SOPS_KMS_ARN`` and ``SOPS_PGP_FP`` environment variables can
take multiple keys separated by commas. All spaces are trimmed.

By default, editing is done in vim. Set the env variable ``$EDITOR``
to use a different editor.

Mozilla Services - ulfr, relud - 2015
"""

# A list of KMS ARNs either provided on the command line or retrieved
# from the user environment
SOPS_KMS_ARN = ""

# A list of PGP fingeprints either provided on the command line or
# retrieved from the user environment
SOPS_PGP_FP = ""

DEFAULT_YAML = """# Welcome to SOPS. This is the default template.
# Remove these lines and add your data.
# Don't modify the `sops` section, it contains key material.
example_key: example_value
example_array:
    - example_value1
    - example_value2
example_multiline: |
    this is a
    multiline
    entry
"""


def main():
    argparser = argparse.ArgumentParser(
        usage='sops <file>',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Encrypted secrets editor',
        epilog=dedent(DESC))
    argparser.add_argument('file',
                           help="file to edit; create it if it doesn't exist")
    argparser.add_argument('-k', '--kms', dest='kmsarn',
                           help="ARN of KMS key used for encryption")
    argparser.add_argument('-g', '--pgp', dest='pgpfp',
                           help="fingerprint of PGP key for decryption")
    argparser.add_argument('-d', '--decrypt', action='store_true',
                           dest='decrypt',
                           help="decrypt <file> and print it to stdout")
    argparser.add_argument('-e', '--encrypt', action='store_true',
                           dest='encrypt',
                           help="encrypt <file> and print it to stdout")
    argparser.add_argument('-i', '--in-place', action='store_true',
                           dest='in_place',
                           help="write output back to <file> instead "
                                "of stdout for encrypt/decrypt")
    argparser.add_argument('-r', '--rotate', action='store_true',
                           dest='rotate',
                           help="generate a new data encryption key and "
                                "encrypt all values with the new key")
    argparser.add_argument('--input-type', dest='input_type',
                           help="input type (yaml, json, ...), "
                                "if undef, use file extension")
    argparser.add_argument('--output-type', dest='output_type',
                           help="output type (yaml, json, ...), "
                                "if undef, use input type")
    args = argparser.parse_args()

    global SOPS_KMS_ARN
    if args.kmsarn:
        SOPS_KMS_ARN = args.kmsarn
    elif 'SOPS_KMS_ARN' in os.environ:
        SOPS_KMS_ARN = os.environ['SOPS_KMS_ARN']

    global SOPS_PGP_FP
    if args.pgpfp:
        SOPS_PGP_FP = args.pgpfp
    elif 'SOPS_PGP_FP' in os.environ:
        SOPS_PGP_FP = os.environ['SOPS_PGP_FP']

    # use input type as output type if not specified
    if args.input_type:
        itype = args.input_type
    else:
        itype = detect_filetype(args.file)

    if args.output_type:
        otype = args.output_type
    else:
        otype = itype

    need_key = False
    is_new_file = False
    try:
        os.stat(args.file)
        # read the encrypted file from disk
        tree = load_tree(args.file, itype)
        tree, need_key = verify_or_create_sops_branch(tree)
    except:
        if args.encrypt or args.decrypt:
            panic("cannot operate on non-existent file", error_code=100)
        print("%s doesn't exist, creating it." % args.file)
        is_new_file = True
        if itype is "yaml":
            tree = ruamel.yaml.load(DEFAULT_YAML, ruamel.yaml.RoundTripLoader)
        else:
            tree = dict()
            tree['data'] = 'Welcome to SOPS. ' + \
                'Remove this line and add your data to the file.'
        tree, need_key = verify_or_create_sops_branch(tree)

    if args.rotate:
        need_key = True

    if args.encrypt:
        # Encrypt mode: encrypt, display and exit
        key, tree = get_key(tree, need_key)

        tree = walk_and_encrypt(tree, key)

    elif args.decrypt:
        # Decrypt mode: decrypt, display and exit
        key, tree = get_key(tree)
        tree = walk_and_decrypt(tree, key)

    else:
        # EDIT Mode: decrypt, edit, encrypt and save
        key, tree = get_key(tree, need_key)

        # we need a stash to save the IV and AAD and reuse them
        # if a given value has not changed during editing
        stash = {'sops': {'has_stash': True}}
        if not is_new_file:
            tree = walk_and_decrypt(tree, key, stash=stash)

        # the decrypted tree is written to a tempfile and an editor
        # is opened on the file
        tmppath = write_file(tree, filetype=otype)
        tmpstamp = os.stat(tmppath)
        run_editor(tmppath)

        # verify if file has been modified, and if not, just exit
        tmpstamp2 = os.stat(tmppath)
        if tmpstamp == tmpstamp2:
            os.remove(tmppath)
            panic("%s has not been modified, exit without writing" % args.file,
                  error_code=200)

        # encrypt the tree
        tree = load_tree(tmppath, otype)
        os.remove(tmppath)
        tree = walk_and_encrypt(tree, key, stash)

    # if we're in -e or -d mode, and not in -i mode, display to stdout
    if (args.encrypt or args.decrypt) and not args.in_place:
        write_file(tree, path='/dev/stdout', filetype=otype)

    # otherwise, write the tree to a file
    else:
        path = write_file(tree, path=args.file, filetype=otype)
        print("file written to %s" % (path), file=sys.stderr)


def detect_filetype(file):
    """Detect the type of file based on its extension.
    Return a string that describes the format: `text`, `yaml`, `json`
    """
    base, ext = os.path.splitext(file)
    if (ext == '.yaml') or (ext == '.yml'):
        return 'yaml'
    elif ext == '.json':
        return 'json'
    return 'text'


def get_key(tree, need_key=False):
    """Obtain a 256 bits symetric key.

    If the document contain an encrypted key, try to decrypt it using
    KMS or PGP. Otherwise, generate a new random key.

    """
    if need_key:
        # if we're here, the tree doesn't have a key yet. generate
        # one and store it in the tree
        print("please wait while a data encryption key is being generated"
              " and stored securely", file=sys.stderr)
        key = os.urandom(32)
        tree = encrypt_key_with_kms(key, tree)
        tree = encrypt_key_with_pgp(key, tree)
        return key, tree
    key = get_key_from_kms(tree)
    if not (key is None):
        return key, tree
    key = get_key_from_pgp(tree)
    if not (key is None):
        return key, tree
    panic("[error] couldn't retrieve a key to encrypt/decrypt the tree",
          error_code=128)


def write_file(tree, path=None, filetype=None):
    """Write the tree content in a file using filetype format.

    Write the content of `tree` encoded using the format defined by
    `filetype` at the location `path`.
    If `path` is not defined, a tempfile is created.
    if `filetype` is not defined, tree is treated as a blob of data.

    Return the path of the file written.

    """
    if path:
        fd = open(path, "wb")
    else:
        fd = tempfile.NamedTemporaryFile(suffix="."+filetype, delete=False)
        path = fd.name
    if filetype == "yaml":
        fd.write(ruamel.yaml.dump(tree, Dumper=ruamel.yaml.RoundTripDumper,
                                  indent=4).encode('utf-8'))
    elif filetype == "json":
        fd.write(json.dumps(tree, sort_keys=True, indent=4).encode('utf-8'))
    else:
        if 'data' in tree:
            # add a newline if there's none
            if tree['data'][-1:] != '\n':
                tree['data'] += '\n'
            fd.write(tree['data'].encode('utf-8'))
        if 'sops' in tree:
            jsonstr = json.dumps(tree['sops'], sort_keys=True)
            fd.write(("SOPS=%s" % jsonstr).encode('utf-8'))
    fd.close()
    return path


def run_editor(path):
    """Open the text editor on the given file path."""
    editor = None
    if 'EDITOR' in os.environ:
        editor = os.environ['EDITOR']
    else:
        process = subprocess.Popen(["which", "vim", "nano"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            editor = line.strip()
            break

    if editor:
        subprocess.call([editor, path])
    else:
        panic("Please define your EDITOR environment variable.", 201)
    return


def panic(msg, error_code=1):
    print(msg, file=sys.stderr)
    sys.exit(error_code)
