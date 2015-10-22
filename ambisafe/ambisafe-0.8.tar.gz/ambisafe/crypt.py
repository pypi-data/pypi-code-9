from hashlib import pbkdf2_hmac

from Crypto import Random
from Crypto.Cipher import AES

ITERATIONS = 1000
KEY_LENGTH = 32
BLOCK_SIZE = AES.block_size

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

def generate_iv():
    return Random.get_random_bytes(BLOCK_SIZE)


class Crypt(object):
    def __init__(self, password):
        self.password = password

    def _derive_key(self, salt):
        return pbkdf2_hmac('sha512', self.password, salt, ITERATIONS, KEY_LENGTH)

    def encrypt(self, data, salt):
        aes = AES.new(self._derive_key(salt), AES.MODE_CBC,
                      generate_iv())
        return aes.IV.encode('hex'), aes.encrypt(pad(data.decode('hex'))).encode('hex')

    def decrypt(self, encrypted, salt, iv):
        encrypted, salt, iv = str(encrypted), str(salt), str(iv)
        aes = AES.new(self._derive_key(salt), AES.MODE_CBC, iv.decode('hex'))
        return unpad(aes.decrypt(encrypted.decode('hex'))).encode('hex')
