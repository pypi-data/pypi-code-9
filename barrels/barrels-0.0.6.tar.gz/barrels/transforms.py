import hashlib
import binascii
import zlib

def sha1(data):
    d = binascii.b2a_base64(
        hashlib.sha1(data).digest()
        ).strip(" \n=")
    return d

def dumps(data):
    zdata = zlib.compress(data)
    return binascii.b2a_base64(zdata).strip()
    return d

def loads(zdata):
    data = binascii.a2b_base64(zdata)
    d = zlib.decompress(data)
    return d
