from functools import partial
import logging
import json
from .containers import Container
from .transactions import GrantTransaction

logger = logging.getLogger('ambisafe')


class Account(object):
    @classmethod
    def from_server_response(cls, response):
        """
        Creates Account subclass for corresponding security schema from response from Ambisafe KeyServer
        :param response:
        :type response: dict
        :returns: Account -- Account subclass
        """
        logger.debug('Ambisafe.account.Account.from_server_response | creating account from response: {}'
                     .format(response))
        account_id = response['account']['externalId']
        security_schema = response['account']['securitySchemaName']

        address = response['account']['address']
        if security_schema == 'Wallet4':
            containers = {}
            for role, container in response.get('containers', {}).items():
                try:
                    del container['role']
                except KeyError:
                    pass
                containers[role] = Container.from_server_response(**container)
            return Wallet4Account(account_id, user_container=containers['USER'],
                                  operator_container=containers['OPERATOR'],
                                  address=address)
        elif security_schema == 'Simple':
            return SimpleAccount(account_id, address)
        elif security_schema == 'CurrencyIssuer':
            return CurrencyIssuerAccount(account_id, response['containers'], address=address)
        else:
            raise NotImplementedError('This security schema is not implemented')

    def as_dict(self):
        """
        Returns dict representations of account
        :return: dict
        """
        raise NotImplemented

    def to_json(self):
        """
        Returns json representations of account
        :return: str
        """
        return json.dumps(self.as_dict())


class SimpleAccount(Account):
    def __init__(self, account_id, address=None, currency='BTC'):
        """
        Base account class
        :param account_id: ID of account
        :type account_id: int or basestring
        :param address:
        :type address: basestring
        :param currency:
        :type currency: basestring
        :return:
        """
        self.id = account_id
        self.currency = currency
        self.address = address
        self._security_schema = 'Simple'

    def as_dict(self):
        """
        Returns dict representations of account
        :return: dict
        """
        return {
            'id': self.id,
            'currency': self.currency,
            'security_schema': self._security_schema,
        }

    def __repr__(self):
        return '<SimpleAccount id={} address={}>'.format(self.id, self.address)


class Wallet4Account(Account):
    def __init__(self, account_id, operator_container=None, user_container=None, address=None, currency='BTC'):
        """
        Creates Wallet4 account object
        :param account_id:
        :type account_id: basestring or int
        :param operator_container:
        :type operator_container: Container
        :param user_container:
        :type user_container: Container
        :param address:
        :type address: basestring
        :param currency:
        :type currency: basestring
        :return:
        """
        assert isinstance(user_container, Container)
        assert isinstance(operator_container, Container)
        self.user_container = user_container
        self.operator_container = operator_container
        self.id = account_id
        self.currency = currency
        self.address = address
        self._security_schema = 'Wallet4'

    def as_dict(self):
        """
        Returns dict representations of account
        :return: dict
        """
        return {
            'id': self.id,
            'currency': self.currency,
            'security_schema': self._security_schema,
            'containers': {
                'USER': self.user_container,
                'OPERATOR': self.operator_container,
            },
        }

    def sign(self, transaction, container_name, secret):
        if container_name == 'USER':
            container = self.user_container
        elif container_name == 'OPERATOR':
            container = self.operator_container
        else:
            raise ValueError('container_name should be "USER" or "OPERATOR"')

        private_key = container.get_private_key(secret)
        sign = partial(container.sign, private_key=private_key)
        signed_sighashes = map(sign, transaction.sighashes)

        if container_name == 'USER':
            transaction.user_signatures = signed_sighashes
        elif container_name == 'OPERATOR':
            transaction.operator_signatures = signed_sighashes

        return transaction

    def __repr__(self):
        return '<Wallet4Account id={} address={}>'.format(self.id, self.address)


class CurrencyIssuerAccount(Account):
    def __init__(self, account_id, containers, address, currency=None):
        self._security_schema = 'CurrencyIssuer'
        self.account_id = account_id
        self.address = address
        self.containers = containers
        self.currency = currency

    def sign(self, transaction, container_number, secret):
        if not isinstance(transaction, GrantTransaction):
            raise ValueError('transaction should be instance of GrantTransaction class')
        container = self.containers[str(container_number)]
        private_key = container.get_private_key(secret)
        sign = partial(container.sign, private_key=private_key)
        signed_sighashes = map(sign, transaction.sighashes)
        transaction.add_signature(container_number, signed_sighashes)
