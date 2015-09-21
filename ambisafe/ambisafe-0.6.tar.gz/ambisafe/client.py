from base64 import b64encode
import calendar
from datetime import datetime
import logging
import json
from hashlib import sha512
import hmac
import re
import requests

from .account import Account
from .containers import Container
from .exc import ClientError, ServerError
from .transactions import BaseTransaction, Wallet4Transaction, RecoveryTransaction, GrantTransaction

logger = logging.getLogger('ambisafe')


class Client(object):
    def __init__(self, ambisafe_server, secret, api_key, api_secret):
        if not re.match(r'^(http|https)://', ambisafe_server):
            raise ValueError('ambisafe_server should be http/https URI')
        self.ambisafe_server = ambisafe_server
        self.secret = secret
        self.api_key = api_key
        self.api_secret = api_secret

    def create_simple_account(self, account_id, currency='BTC'):
        """
        Create account with Simple security schema
        :param account_id: int|str
        :param currency: str
        :return:
        """
        logger.debug('Creating account with Simple security schema: account_id: {}, currency: {}'
                     .format(account_id, currency))

        response = self.make_request('POST', '/accounts', json.dumps({
            'id': str(account_id),
            'currency': currency,
            'security_schema': 'Simple',
        }))

        return Account.from_server_response(response)

    def create_wallet4_account(self, account_id, user_container, operator_container, currency='BTC'):
        """
        Create account with Wallet4 security schema
        :param account_id: int|str
        :param user_container: ambisafe.account.Container
        :param operator_container: ambisafe.account.Container
        :param currency: str
        :return:
        """
        logger.debug('Creating account with Wallet4 security schema: account_id: {}, currency: {} '
                     'containers: (user: {}, operator: {})'
                     .format(account_id, currency, user_container, operator_container))

        containers = {
            "USER": user_container.as_request(),
            "OPERATOR": operator_container.as_request(),
        }
        response = self.make_request('POST', '/accounts', json.dumps({
            'id': str(account_id),
            'currency': currency,
            'security_schema': 'Wallet4',
            'containers': containers,
        }))

        return Account.from_server_response(response)

    def create_currency_issuer_account(self, account_id, signatures_required, containers, currency):
        logger.debug('Creating account with CurrencyIssuer security schema: account_id: {}, currency: {} '
                     'containers: {} signatures_required: {}'
                     .format(account_id, currency, containers, signatures_required))
        if any(not isinstance(container, Container) for container in containers):
            raise ValueError("containers should be a list of Container instances")

        containers = [dict(role=str(i), **container.__dict__) for i, container in enumerate(containers)]
        response = self.make_request('POST', '/accounts', json.dumps({
            'id': str(account_id),
            'currency': currency,
            'security_schema': 'CurrencyIssuer',
            'signatures_required': signatures_required,
            'containers': containers,
        }))
        return Account.from_server_response(response)

    def update_wallet4_account(self, account_id, user_container, operator_container,
                               currency='BTC', regenerate_server_container=False):
        containers = {
            "USER": user_container.as_request(),
            "OPERATOR": operator_container.as_request(),
        }
        return Account.from_server_response(self.make_request('PUT', '/accounts', json.dumps({
            'id': account_id,
            'currency': currency,
            'security_schema': 'Wallet4',
            'containers': containers,
            'regenerate_server_container': regenerate_server_container,
        })))

    def get_balance(self, account_id, currency='BTC'):
        return float(
            self.make_request('GET', '/balances/{currency}/{external_id}'
                              .format(currency=currency, external_id=account_id))['balance']
        )

    def get_account(self, account_id, currency='BTC'):
        return Account.from_server_response(
            self.make_request('GET', '/accounts/{external_id}/{currency}'
                              .format(external_id=account_id, currency=currency))
        )

    def build_transaction(self, account_id, currency, destination, amount):
        body = {
            "destination": destination,
            "amount": amount,
        }
        return Wallet4Transaction(**self.make_request('POST', '/transactions/build/{external_id}/{currency}'
                                                              .format(external_id=account_id, currency=currency),
                                                      body=json.dumps(body)))

    def submit(self, account_id, transaction, currency):
        if not isinstance(transaction, BaseTransaction):
            raise ValueError('transaction should be instance of BaseTransaction class')
        return self.make_request('POST', '/transactions/submit/{external_id}/{currency}'
                                 .format(external_id=account_id, currency=currency),
                                 body=transaction.to_json())

    def sign_wallet4_transaction(self, transaction, account_id, currency):
        account = self.get_account(account_id, currency)
        return account.sign(transaction, 'OPERATOR', self.secret)

    def cosign_wallet4_and_submit(self, transaction, account_id, currency='BTC'):
        transaction = self.sign_wallet4_transaction(transaction, account_id, currency)
        return self.submit(account_id, transaction, currency)

    def build_recovery_transaction(self, account_id, currency, old_address):
        response = self.make_request(
            'POST',
            '/transactions/build_recovery/{external_id}/{currency}/{address}'
            .format(external_id=account_id, currency=currency, address=old_address)
        )
        logger.debug('response: {}'.format(response))
        return RecoveryTransaction(response['operator'], response['recovery_transaction'], response['account_id'])

    def cosign_and_recovery(self, transaction, account_id, currency='BTC'):
        transaction = self.sign_wallet4_transaction(transaction, account_id, currency)
        return self.submit(account_id, transaction, currency)

    def build_grant_transaction(self, account_id, currency, destination, amount, signatures_required):
        body = {
            "destination": destination,
            "amount": str(amount),
            "signatures_required": str(signatures_required),
            "operation_type": "grant"
        }
        transaction = self.make_request('POST',
                                        '/transactions/build/{id}/{currency}'.format(id=account_id, currency=currency),
                                        json.dumps(body))
        return GrantTransaction(**transaction)

    def make_request(self, method, uri, body=None):
        url = self.ambisafe_server + uri
        utctime = datetime.utcnow()
        nonce = int(calendar.timegm(utctime.timetuple()) * 10 ** 3
                    + utctime.microsecond * 10 ** -3)
        message = "{}\n{}\n{}\n".format(nonce, method, url)
        if body:
            message += body
        digest = hmac.new(self.api_secret, msg=message, digestmod=sha512)
        signature = b64encode(digest.digest()).replace('\n', '')
        headers = {
            'API-key': self.api_key,
            'signature': signature,
            'timestamp': nonce,
            'Accept': 'application/json'
        }
        if method in ['POST', 'PUT']:
            headers['Content-Type'] = 'application/json'
        logger.debug('Request to ambisafe KeyServer: method: {}, url: "{}", headers: {}, data: {}'
                     .format(method, url, headers, body))
        response = requests.request(method, url, headers=headers, data=body)
        logger.debug('Response from ambisafe KeyServer: status: {}, text: {}'
                     .format(response.status_code, response.text))
        try:
            response_data = response.json()
        except ValueError, e:
            # ValueError is parent of JSONDecodeError
            raise ServerError(e.message, '')

        if not response.ok:
            if 400 <= response.status_code < 500:
                raise ClientError(response_data['message'], response_data['error'])
            elif 500 <= response.status_code < 600:
                raise ServerError(response_data['message'], response_data['error'])

        return response_data
