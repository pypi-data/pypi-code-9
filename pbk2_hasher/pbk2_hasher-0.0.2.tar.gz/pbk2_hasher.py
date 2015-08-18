'''
    pbk2_hasher
    ~~~~~~~~~~~

    A pbk2 hasher implementation that is compatible with django's auth.hashers.
'''

import base64
import hashlib
import hmac
import random


def check_password(password, encoded, setter=None, preferred='default'):
    '''
    Returns a boolean of whether the raw password matches the three part
    encoded digest.

    WARNING: it won't regenerate the password.
    '''
    if password is None:
        return False

    hasher = PBKDF2PasswordHasher()
    return hasher.verify(password, encoded)


def make_password(password, salt=None, hasher=None):
    '''
    Turn a plain-text password into a hash for database storage.
    '''
    assert password is not None, 'password must be a string'

    hasher = PBKDF2PasswordHasher()

    if not salt:
        salt = hasher.salt()

    return hasher.encode(password, salt)


def force_bytes(s):
    if isinstance(s, bytes):
        return s
    if isinstance(s, str):
        return str.encode(s, 'u8')
    raise ValueError(s)


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))


def pbkdf2(password, salt, iters, dklen=0, digest=None):
    if digest is None:
        digest = hashlib.sha256
    if not dklen:
        dklen = None
    password = force_bytes(password)
    salt = force_bytes(salt)
    return hashlib.pbkdf2_hmac(digest().name, password, salt, iters, dklen)


class PBKDF2PasswordHasher(object):
    '''
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256.
    The result is a 64 byte binary string. Iterations may be changed safely
    but you must rename the algorithm if you change SHA256.
    '''
    algorithm = 'pbkdf2_sha256'
    iterations = 24000
    digest = hashlib.sha256

    def salt(self):
        return get_random_string()

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return '{}${}${}${}'.format(
            self.algorithm,
            iterations,
            salt,
            hash
        )

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        if not algorithm == self.algorithm:
            return False
        encoded_2 = self.encode(password, salt, int(iterations))
        return hmac.compare_digest(force_bytes(encoded),
                                   force_bytes(encoded_2))
