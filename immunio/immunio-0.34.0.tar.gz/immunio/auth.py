import hashlib
import hmac


def get_hmac(secret, data):
    secret = secret.encode("ascii")
    data = data.encode("ascii")
    sig = hmac.new(secret, data, hashlib.sha1).hexdigest()
    return sig
