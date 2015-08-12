import logging
import json
from uuid import uuid4
from ecdsa import SigningKey, SECP256k1, util
from pybitcointools import privkey_to_pubkey, compress

from .crypt import Crypt

logger = logging.getLogger('ambisafe')


class Container(object):
    def __init__(self, public_key, data, iv, salt):
        self.public_key = public_key
        self.data = data
        self.iv = iv
        self.salt = salt

    @classmethod
    def generate(cls, secret):
        key = SigningKey.generate(curve=SECP256k1)
        private_key = key.to_string().encode('hex')
        compressed_public_key = compress(privkey_to_pubkey(private_key))
        logger.debug('Generate keys: {} {}'.format(compressed_public_key, private_key))
        crypt = Crypt(secret)
        salt = str(uuid4())
        iv, encrypted_private_key = crypt.encrypt(private_key, salt)
        return cls(compressed_public_key, encrypted_private_key, iv, salt)

    @classmethod
    def from_server_response(cls, publicKey, data, iv, salt):
        return cls(publicKey, data, iv, salt)

    def get_private_key(self, secret):
        crypt = Crypt(secret)
        return crypt.decrypt(self.data, self.salt, self.iv)

    def sign(self, message, private_key):
        key = SigningKey.from_string(private_key.decode('hex'), curve=SECP256k1)
        sig = key.sign_digest(message.decode('hex'), sigencode=util.sigencode_der) + '01'.decode('hex')
        return sig.encode('hex')

    def __getitem__(self, item):
        return self.__dict__[item]


class Transaction(object):
    def __init__(self, hex, fee, sighashes, operator_signatures=None, user_signatures=None):
        self.hex = hex
        self.fee = fee
        self.sighashes = sighashes
        self.operator_signatures = operator_signatures
        self.user_signatures = user_signatures

    def to_json(self):
        return json.dumps(self.__dict__)


class RecoveryTransaction(Transaction):
    def __init__(self, operator_container, *args, **kwargs):
        self.operator_container = operator_container
        super(RecoveryTransaction, self).__init__(*args, **kwargs)


class Account(object):
    def __init__(self, account_id, containers, security_schema, address=None, currency='BTC'):
        self.id = account_id
        self.currency = currency
        self.security_schema = security_schema
        self.containers = containers
        self.address = address

    @classmethod
    def from_server_response(cls, response):
        logger.debug('Ambisafe.account.Account.from_server_response | creating account from response: {}'
                     .format(response))
        account_id = response['account']['externalId']
        security_schema = response['account']['securitySchemaName']
        containers = {}
        for role, container in response.get('containers', {}).items():
            try:
                del container['role']
            except KeyError:
                pass
            containers[role] = Container.from_server_response(**container)
        return cls(account_id, containers, security_schema, address=response['account']['address'])

    @property
    def operator_container(self):
        return self.containers['OPERATOR']

    @property
    def user_container(self):
        return self.containers['USER']

    def as_dict(self):
        return {
            'id': self.id,
            'currency': self.currency,
            'security_schema': self.security_schema,
            'containers': self.containers,
        }

    def to_json(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return '<Account id={}>'.format(self.id)
