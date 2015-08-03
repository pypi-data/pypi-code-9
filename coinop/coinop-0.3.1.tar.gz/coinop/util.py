from hashlib import sha256
from binascii import hexlify, unhexlify

# Could be replaced with bitcoin.core.serialize.Hash
def double_hash (s):
    return sha256(sha256(s).digest()).digest()

def dict_subset(d, *args):
    return dict((k, d[k]) for k in args)
