
"""Replica of ImpayMember library."""

import hashlib
from base64 import b64encode as base64_encode, b64decode as base64_decode
from Crypto.Cipher import AES
from . import env


BLOCK_SIZE = 16


def sha256Encrypt(s):
    return hashlib.sha256(s).hex_digest()


def pad(s):
    length = len(s)
    pad_size = BLOCK_SIZE - (length % BLOCK_SIZE)
    padding = pad_size * chr(pad_size)
    return s + padding


def unpad(s):
    pad_size = ord(s[-1])
    return s[:-pad_size]


class Library(object):
    def __init__(self, env=env.default):
        self.env = env

    def encrypt_01(self, s):
        encrypted = self.encrypt_function(s)
        return encrypted

    def encrypt_function(self, s):
        encrypted = self.encrypt_block(pad(s))
        encoded = base64_encode(encrypted)
        return encoded

    # AES encrypt process
    def encrypt_block(self, plain_text, env=env.default):
        aes = AES.new(self.env.CRYPT_AES_KEY, AES.MODE_ECB)
        cipher_text = aes.encrypt(plain_text)
        return cipher_text

    def decrypt_01(self, s):
        decrypted = self.decrypt_function(s)
        return decrypted

    def decrypt_function(self, s):
        decoded = base64_decode(s)
        decrypted = self.decrypt_block(decoded)
        return decrypted

    def decrypt_block(self, cipher_text):
        aes = AES.new(self.env.CRYPT_AES_KEY, AES.MODE_ECB)
        plain_text = aes.decrypt(cipher_text)
        return unpad(plain_text)

    def decrypt_02(self, s):
        decrypted = self.impay_decrypt(s)
        return decrypted

    def impay_decrypt(self, s):
        decoded = s.decode('hex')
        aes = AES.new(
            self.env.CRYPT_IMPAY_KEY, AES.MODE_CBC, self.env.IMPAY_IV)
        plain_text = aes.decrypt(decoded)
        return unpad(plain_text)
