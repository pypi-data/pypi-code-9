import logging
from uuid import uuid4
from ecdsa import SECP256k1, SigningKey, util
from pybitcointools import compress, privkey_to_pubkey
from ambisafe.crypt import Crypt

logger = logging.getLogger('ambisafe')


class Container(object):
    def __init__(self, public_key, data, iv, salt):
        """
        Creates container.
        :param public_key: Public key
        :param data: Encrypted private_key
        :param iv: IV
        :param salt: Salt
        :return: Container
        """
        self.publicKey = public_key
        self.data = data
        self.iv = iv
        self.salt = salt

    @classmethod
    def generate(cls, secret):
        """
        Generating new container encrypted with secret
        :param secret:
        :type secret: basestring
        :return: Container
        """
        key = SigningKey.generate(curve=SECP256k1)
        private_key = key.to_string().encode('hex')
        compressed_public_key = compress(privkey_to_pubkey(private_key))
        crypt = Crypt(secret)
        salt = str(uuid4())
        iv, encrypted_private_key = crypt.encrypt(private_key, salt)
        return cls(compressed_public_key, encrypted_private_key, iv, salt)

    @classmethod
    def from_server_response(cls, publicKey, data, iv, salt):
        """
        Creating Container object from Ambisafe KeyServer response
        :param publicKey:
        :param data:
        :param iv:
        :param salt:
        :return:
        """
        return cls(publicKey, data, iv, salt)

    def get_private_key(self, secret):
        """
        Get decrypted private key from Container using secret
        :param secret:
        :return: str
        """
        crypt = Crypt(secret)
        private_key = crypt.decrypt(self.data, self.salt, self.iv)
        if not private_key:
            raise ValueError('Wrong secret')
        return private_key

    def sign(self, message, private_key):
        """
        Sign message with private key
        :param message:
        :param private_key:
        :return: str
        """
        key = SigningKey.from_string(private_key.decode('hex'), curve=SECP256k1)
        sig = key.sign_digest(message.decode('hex'), sigencode=util.sigencode_der) + '01'.decode('hex')
        logger.debug('pub: {} priv: {} sighash: {} signed: {}'
                     .format(self.publicKey, private_key, message, sig.encode('hex')))
        return sig.encode('hex')

    def __getitem__(self, item):
        return self.__dict__[item]

    def as_response(self):
        """
        Get container dict in response format
        :return: dict
        """
        return self.__dict__

    def as_request(self):
        """
        Get container dict in request format
        :return: dict
        """
        container = self.__dict__
        # work around different request and response formats
        container['public_key'] = container.pop('publicKey')
        return container
