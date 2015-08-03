from __future__ import unicode_literals
from future.utils import iteritems
from binascii import hexlify, unhexlify

from os import urandom
from pycoin.key.BIP32Node import BIP32Node

from .script import Script
from .keys import PrivateKey, PublicKey

import bitcoin.base58 as base58

# A MultiWallet maintains any number of BIP 32 HDW trees, treating them
# as parallel structures.  Given a path, the MultiWallet can produce
# a MultiNode containing the appropriate nodes for each tree.  These
# nodes can be used in multi-sig applications.

# The HDW trees need not be private; in many applications, you specifically
# need to use some public trees and some private trees.

# MultiWallet trees are named, allowing them to be distinguished easily.

class MultiWallet(object):

    # Given a list of tree names, create a MultiWallet containing private trees.
    # If `entropy` is true, return a 2-tuple of a dict of name:secret pairs and
    # a MultiWallet
    @classmethod
    def generate(cls, names, entropy=False):
        secrets = {}
        for name in names:
            secrets[name] = hexlify(urandom(32)).decode('utf-8')

        if entropy:
            return secrets, cls(private_seeds=secrets)
        return cls(private_seeds=secrets)


    # The private and public arguments are dicts that contain HDW seed
    # strings in WIF format, keyed by name.
    # private_seeds is a dict of the same form but containing raw entropy
    # instead of a node
    def __init__(self, private={}, public={}, private_seeds={}):
        # It is possible to distinguish between private and public seeds
        # based on the string content.  Consider modifying this function
        # to take merely one dict of seeds.  Trees should still be stored
        # separately.
        self.trees = {}
        self.private_trees = {}
        self.public_trees = {}

        def treegen(value, entropy=False):
            if entropy:
                # this method also takes a netcode parameter, but we don't care
                # what network pycoin thinks this node is, because we only use it
                # for key derivation.
                return BIP32Node.from_master_secret(unhexlify(value))
            else:
                # this method will infer a network from the header bytes. We
                # don't care right now for the same reason as above, but we will
                # if Gem's API stops returning 'xpub' as the pubkey header bytes
                # because if pycoin doesn't recognize a header it will error.
                return BIP32Node.from_hwif(value)

        for name, seed in iteritems(private):
            tree = treegen(seed)
            self.private_trees[name] = self.trees[name] = tree

        for name, seed in iteritems(private_seeds):
            tree = treegen(seed, True)
            self.private_trees[name] = self.trees[name] = tree

        for name, seed in iteritems(public):
            tree = BIP32Node.from_hwif(seed)
            self.public_trees[name] = self.trees[name] = tree

    def to_dict(self):
        return dict(private=self.private_seeds(), public=self.public_seeds())

    def private_wif(self, name):
        try:
            return self.private_trees[name].hwif(as_private=True)
        except KeyError:
            raise Exception("No private tree for '{0}'".format(name))

    def private_wifs(self):
        return { name: self.private_wif(name)
                 for name in self.private_trees.keys() }

    def public_wif(self, name):
        tree = self.public_trees.get(name, None)
        if not tree:
            tree = self.private_trees.get(name, None)
        if not tree:
            raise Exception("No public tree for '{0}'".format(name))
        return tree.hwif()

    def public_wifs(self):
        return { name: self.public_wif(name)
                 for name in self.public_trees.keys() }

    # Given a wallet path, returns a MultiNode for that path.
    # The path string should either begin with 'm/' or be relative to the master
    # node.
    def path(self, path):
        _path = path[2:] if path[:2] == 'm/' else path

        private = { name: tree.subkey_for_path(_path)
                    for name, tree in iteritems(self.private_trees) }

        public = { name: tree.subkey_for_path(_path)
                   for name, tree in iteritems(self.public_trees) }

        return MultiNode(path, private=private, public=public)

    # Determines whether the script included in an Output was generated
    # from this wallet.
    # TODO: support multi-network
    def is_valid_output(self, output):
        # TODO: better error handling in case no wallet_path is found.
        # May also be better to take the wallet_path as an argument to
        # the function.
        node = self.path(output.metadata['wallet_path'])

        generated_script = node.p2sh_script().to_string()
        given_script = output.script.to_string()
        return generated_script == given_script

    # Returns a list of signature dicts, corresponding to the inputs
    # for the supplied transaction.
    def signatures(self, transaction):
        return list(map(self.sign_input, transaction.inputs))

    # Given an Input (the output of which must contain a wallet_path in
    # its metadata) return a dictionary of signatures.  The dict keys
    # are the names of the private trees.
    def sign_input(self, input):
        path = input.output.metadata['wallet_path']
        node = self.path(path)
        sig_hash = input.sig_hash(node.script())
        return node.signatures(sig_hash)


# Manages any number of BIP 32 nodes (private and/or public) derived from
# a given path.
class MultiNode(object):

    def __init__(self, path, private={}, public={}):
        self.path = path
        self.private = private
        self.public = public

        self.private_keys = {}
        self.public_keys = {}

        for name, node in iteritems(private):
            priv = PrivateKey.from_secret(node._secret_exponent_bytes)
            self.private_keys[name] = priv

            pub = priv.public_key()
            self.public_keys[name] = pub

        for name, node in iteritems(public):
            pub = PublicKey.from_pair(node.public_pair())
            self.public_keys[name] = pub


    def script(self, m=2):
        names = sorted(self.public_keys.keys())
        keys = [self.public_keys[name].compressed() for name in names]

        return Script(public_keys=keys, needed=m)

    p2sh_script = script

    # Returns the P2SH address for a m-of-n multisig script using the
    # public keys derived for this node.
    def address(self, m=2, network=None):
        return self.script(m).p2sh_address(network=network)

    # Returns a dict of signatures, keyed by the tree names.
    def signatures(self, value):
        names = sorted(self.private_keys.keys())
        return {name: base58.encode(self.sign(name, value)) for name in names}

    def sign(self, name, value):
        try:
            key = self.private_keys[name]
            # Append a "hashtype" byte to the signature.
            # \x01 means the hash type is SIGHASH_ALL.  Other hashtypes are not
            # often used.
            # https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
            return key.sign(value) + b'\x01'
        except KeyError:
            raise Exception("No such key: '{0}'".format(name))


    # TODO: pretty sure this is never used and doesn't work.
    # Generate the script_sig for a set of signatures.
    def script_sig(self, signatures):
        self.script.p2sh_sig(signatures=signatures)
