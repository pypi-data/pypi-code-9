# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import Blowfish

# Funcao para encriptar de drcriptogravar dados
class Criptografia(object):
    def __init__(self, secret_key, id, salt):
        secret_key = secret_key[:11] + secret_key[-12:]
        id = str(id).ljust(10, 'x')
        salt = salt[:23]
        self.chave = '%s%s%s' % (secret_key, id, salt)

    def encriptar(self, string):
        """Encripta um código qualquer usando uma chave dinâmica."""
        encryption_object = Blowfish.new(self.chave)
        padding = ''
        if (len(string) % 8) != 0:
            padding = 'x' * (8 - (len(string) % 8))
        return base64.b64encode(encryption_object.encrypt(string + padding))

    def decriptar(self, string):
        """Decripta um código qualquer usando uma chave dinâmica."""
        encryption_object = Blowfish.new(self.chave)
        return encryption_object.decrypt(base64.b64decode(string)).rstrip('x')