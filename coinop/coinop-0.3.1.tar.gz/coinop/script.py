from __future__ import unicode_literals
from future.builtins import bytes

from binascii import hexlify, unhexlify

from bitcoin.core.script import (CScript, OPCODES_BY_NAME, OP_CHECKMULTISIG,
    OP_HASH160, OP_EQUAL, CScriptTruncatedPushDataError, CScriptInvalidError)

from bitcoin.wallet import CBitcoinAddress
from bitcoin.core import b2x, Hash, Hash160
from bitcoin.base58 import encode, decode

def encode_address(hash160, network):
    if network == "mainnet":
        version = 5
    elif network == "testnet":
        version = 196
    else:
        raise ValueError("Unknown network")

    data = bytes([version]) + hash160
    checksum = Hash(data)[0:4]
    return encode(data + checksum)


# Given a script in human-readable "asm" form, returns the script as a
# byte string.
# Adapted from python-bitcoinlib's tests
def from_string(string):

    # TODO: this should probably go in a util package.
    def ishex(s):
        return set(s).issubset(set('0123456789abcdefABCDEF'))

    r = []

    # Create an opcodes_by_name table with both OP_ prefixed names and
    # shortened ones with the OP_ dropped.
    opcodes_by_name = {}
    for name, code in OPCODES_BY_NAME.items():
        opcodes_by_name[name] = code
        opcodes_by_name[name[3:]] = code

    for word in string.split():
        if word.isdigit() or (word[0] == '-' and word[1:].isdigit()):
            r.append(CScript([int(word)]))
        elif ishex(word):
            word_bytes = unhexlify(word.encode('utf8'))
            push_code = bytes([len(word_bytes)])
            r.append(push_code + word_bytes)

        elif len(word) >= 2 and word[0] == "'" and word[-1] == "'":
            r.append(CScript([bytes(word[1:-1].encode('utf8'))]))
        elif word in opcodes_by_name:
            r.append(CScript([opcodes_by_name[word]]))
        else:
            raise ValueError("Error parsing script: %r" % string)

    return CScript(b''.join(r))

def from_p2sh_address(address):
    return CScript([OP_HASH160, CBitcoinAddress(address), OP_EQUAL])


def multisig(public_keys, needed):
    return CScript([needed] + public_keys + [len(public_keys), OP_CHECKMULTISIG])


# Given a byte string representing a script, returns the human readable
# "asm" format.
# Adapted from python-bitcoinlib's bitcoin.core.script.CScript.__repr__,
# which returns a string with the class name prefixed.
def cscript_to_string(cscript):
    def to_s(o):
        if isinstance(o, bytes):
            return b2x(o)
        else:
            return repr(o)

    ops = []
    i = iter(cscript)
    while True:
        op = None
        try:
            op = to_s(next(i))
        except CScriptTruncatedPushDataError as err:
            op = '%s...<ERROR: %s>' % (to_s(err.data), err)
            break
        except CScriptInvalidError as err:
            op = '<ERROR: %s>' % err
            break
        except StopIteration:
            break
        finally:
            if op is not None:
                ops.append(op)
    return ' '.join(ops)



# A wrapper class to make it easier to work with CScript
class Script(object):

    # * cscript - An actual CScript instance
    # * string - The "asm", human-readable form of a Bitcoin script
    # * binary - Byte string representation of a script
    # * hex - Hex representation of a script
    # * p2sh_address - A pay-to-script-hash address
    # * public_keys, needed - the public keys for a multisig script and
    #   the number of signatures needed for valid authorization.
    def __init__(self, cscript=None, string=None, type=None, binary=None,
                 hex=None, p2sh_address=None, public_keys=[], needed=1):
        if cscript:
            self.set_cscript(cscript)
        elif string:
            self.set_cscript(from_string(string))
        elif binary:
            self.set_cscript(CScript(binary))
        elif hex:
            self.set_cscript(CScript(unhexlify(hex)))
        elif p2sh_address:
            self.set_cscript(from_p2sh_address(p2sh_address))
        # TODO: add a branch for handling 'address', which should be able
        # to work with either P2SH or regular addresses
        elif public_keys and needed:
            self.set_cscript(multisig(public_keys, needed))
        else:
            raise Exception("Invalid options")

    def set_cscript(self, cscript):
        self.cscript = cscript

    def to_string(self):
        return cscript_to_string(self.cscript)

    def __str__(self):
        return cscript_to_string(self.cscript)

    def to_hex(self):
        return hexlify(self.cscript)

    def to_binary(self):
        # CScript convenient inherits from `bytes`
        return self.cscript

    def hash160(self):
        return Hash160(self.cscript)

    def p2sh_script(self):
        cscript = self.cscript.to_p2sh_scriptPubKey()
        return Script(cscript=cscript)

    # Returns the P2SH address for this script.  This presumes that the
    # script is one suitable for defining the authorization of an input.
    # E.g. it could be a multi-sig script that contains the M value and
    # the set of public keys to be used (but not any signatures)
    def p2sh_address(self, network):
        return encode_address(self.hash160(), network)
