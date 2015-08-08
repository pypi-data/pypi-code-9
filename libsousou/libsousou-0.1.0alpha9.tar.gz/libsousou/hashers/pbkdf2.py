from collections import OrderedDict
from functools import reduce
import base64
import datetime
import hashlib
import hmac
import operator
import struct

from libsousou.hashers.base import BasePasswordHasher
from libsousou.hashers.base import constant_time_compare
from libsousou.hashers.base import mask_hash
from libsousou.hashers.base import _bin_to_long
from libsousou.hashers.base import _long_to_bin

_ = lambda x: x
__all__ = [
    'PBKDF2PasswordHasherSHA256',
    'PBKDF2PasswordHasherSHA512',
]

YEAR = datetime.date.today().year


def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """
    Implements PBKDF2 as defined in RFC 2898, section 5.2

    HMAC+SHA256 is used as the default pseudo random function.

    As of 2011, 10,000 iterations was the recommended default which
    took 100ms on a 2.2Ghz Core 2 Duo. This is probably the bare
    minimum for security given 1000 iterations was recommended in
    2001. This code is very well optimized for CPython and is only
    four times slower than openssl's implementation. Look in
    django.contrib.auth.hashers for the present default.
    """
    assert iterations > 0
    if not digest:
        digest = hashlib.sha256
    password = password if isinstance(password, bytes) else password.encode()
    salt = salt if isinstance(salt, bytes) else salt.encode()
    hlen = digest().digest_size
    if not dklen:
        dklen = hlen
    if dklen > (2 ** 32 - 1) * hlen:
        raise OverflowError('dklen too big')
    l = -(-dklen // hlen)
    r = dklen - (l - 1) * hlen

    hex_format_string = "%%0%ix" % (hlen * 2)

    inner, outer = digest(), digest()
    if len(password) > inner.block_size:
        password = digest(password).digest()
    password += b'\x00' * (inner.block_size - len(password))
    inner.update(password.translate(hmac.trans_36))
    outer.update(password.translate(hmac.trans_5C))

    def F(i):
        def U():
            u = salt + struct.pack(b'>I', i)
            for j in range(int(iterations)):
                dig1, dig2 = inner.copy(), outer.copy()
                dig1.update(u)
                dig2.update(dig1.digest())
                u = dig2.digest()
                yield _bin_to_long(u)
        return _long_to_bin(reduce(operator.xor, U()), hex_format_string)

    T = [F(x) for x in range(1, l + 1)]
    return b''.join(T[:-1]) + T[-1][:r]


class PBKDF2PasswordHasherSHA256(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256 with 180000 iterations.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = "pbkdf2_sha256"

    # Using an optimistic interpretation of Moore's Law,
    # double the number of iterations for each year. The
    # base value is the OWASP recommendation from 2012.
    iterations =  64000 * 2**(YEAR - 2012)
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        if not iterations:
            iterations = self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('iterations'), iterations),
            (_('salt'), mask_hash(salt)),
            (_('hash'), mask_hash(hash)),
        ])

    def must_update(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        return int(iterations) != self.iterations


class PBKDF2PasswordHasherSHA512(PBKDF2PasswordHasherSHA256):
    algorithm = 'pbkdf2_sha512'
    iterations = 180000
    digest = hashlib.sha512
