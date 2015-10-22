from functools import partial
import json
from random import randint, choice
import string
import unittest
import httpretty
import mock

from ambisafe import Account, Container, Wallet4Transaction, Client, Crypt


def cosign_by_user(self, password, transaction, account_id, currency='BTC'):
    account = self.get_account(account_id, currency)
    container = account.user_container
    private_key = container.get_private_key(password)
    sign = partial(container.sign, private_key=private_key)
    transaction.user_signatures = map(sign, transaction.sighashes)
    return transaction

Client.cosign_by_user = cosign_by_user


class ClientTestCase(unittest.TestCase):
    id = 'test_{}'.format(randint(1, 100000000))
    _get_account_response = '{"account":{"externalId":"%s","currencyFamilySymbol":"BitcoinFamily","securitySchemaName' \
                            '":"Wallet4","address":"3MLbmeUjhiU8Artq2Xp3cdKZzXmocQahpy"},"containers":{"USER":{"publi' \
                            'cKey": "034a94cacac4327feb793047c514b256b326c3c474d73c861407a8709f9901039e", "data": "a0' \
                            'b0cbf2c2697f5141041da8a012149dc4cd82df6f43be8cfc58342ba8e663722178509b667217f2c990ec24ff' \
                            'aeb2ed", "salt": "ca20faef-ac3f-40a6-99c0-500855c03207", "iv": "ff55e03b11dc43adf839c3ae' \
                            'e3632b36"},"OPERATOR":{"publicKey": "034a94cacac4327feb793047c514b256b326c3c474d73c86140' \
                            '7a8709f9901039e", "data": "a0b0cbf2c2697f5141041da8a012149dc4cd82df6f43be8cfc58342ba8e66' \
                            '3722178509b667217f2c990ec24ffaeb2ed", "salt": "ca20faef-ac3f-40a6-99c0-500855c03207", "i' \
                            'v": "ff55e03b11dc43adf839c3aee3632b36"}}}' % id
    _build_transaction_response = '{"hex":"0100000001d2c7543329cc67caf16bdbe2fec1de29f2119c902cb1fc271ab0312e8f4c842b' \
                                  '0000000091000000004c8b5321023acc402315f02158304d2ff6fdb3e08edbc1e052100595c4873b08' \
                                  '73fd36a33a2102a98e0db19265f8da57797384a2cbbb8db33cdf147a6780349a67506d64de2dfb2102' \
                                  '787591a1671fc234f4bd809ed65ac6ab27b63713084e81a295bc9088515e13cc2103c65efb073846e1' \
                                  'c1e3a56f08c29ce79d7c9f5dab5e2c09490985a75c6779cd1c54aeffffffff04ac0200000000000047' \
                                  '5121030c28fe5f18c699a30b62b7d67de92b7493658f2bab2a1806fbf5f0ea7f28e8db21023c3409dd' \
                                  'c09896cdead6d5949b093cd8c94bd18c1fcc5370415ee276f399676852ae22020000000000001976a9' \
                                  '14946cb2e08075bcbaf157e47bcb67eb2b2339d24288ac220200000000000017a9145261efc042151b' \
                                  '5e595797605862128a9842a03487980c00000000000017a914d78608c18942160a642b05733b7786e2' \
                                  'a8d843398700000000","fee":"0.0001 BTC","sighashes":["b3cfce1850fcd9fafa6be899398bb' \
                                  '82327944fbe192b7f43ba1603d6141abb3e"]}'
    _transaction_ok = '{"state":"sending","transaction":"0100000001d2c7543329cc67caf16bdbe2fec1de29f2119c902cb1fc271a' \
                      'b0312e8f4c842b00000000fd6a0100483045022100cb22b4a40b5c7520c1ed808f9514ff29a47b396c8de527758a24' \
                      '8e94fdedd546022001c90fd9fec4ad6188dec59370e47e5fbc90b8623d1effd9d9e1aa83db1f5d3501493046022100' \
                      'e83e4feaa680f5f476116abf6027eb63f005d6bdba3bf17ac0d73bbf5a209407022100bd9d525b7dfe2bc20edcfed0' \
                      'f0e6252f9de8ce0d760cb9fbcb8c153ea21debfe01483045022100a944c93adc0d7a0adf021174bb3fd40921a0b023' \
                      '3ed4c51286eac886346122a2022073c0627906e372d80c046dc8f283c09ddf9aa167ccbdf56019269de9b123713401' \
                      '4c8b5321023acc402315f02158304d2ff6fdb3e08edbc1e052100595c4873b0873fd36a33a2102a98e0db19265f8da' \
                      '57797384a2cbbb8db33cdf147a6780349a67506d64de2dfb2102787591a1671fc234f4bd809ed65ac6ab27b6371308' \
                      '4e81a295bc9088515e13cc2103c65efb073846e1c1e3a56f08c29ce79d7c9f5dab5e2c09490985a75c6779cd1c54ae' \
                      'ffffffff04ac02000000000000475121030c28fe5f18c699a30b62b7d67de92b7493658f2bab2a1806fbf5f0ea7f28' \
                      'e8db21023c3409ddc09896cdead6d5949b093cd8c94bd18c1fcc5370415ee276f399676852ae220200000000000019' \
                      '76a914946cb2e08075bcbaf157e47bcb67eb2b2339d24288ac220200000000000017a9145261efc042151b5e595797' \
                      '605862128a9842a03487980c00000000000017a914d78608c18942160a642b05733b7786e2a8d843398700000000",' \
                      '"transactionHash":"b9beff30a956f37180d7b2e7245677d8b2d9f7728433c7693ee33ac48bd8b0f3"}'

    @classmethod
    def setUpClass(cls):
        cls.client = Client('http://localhost:8080', 'test', 'demo', 'demo')

    @httpretty.activate
    def test_create_account_wallet4(self):
        httpretty.register_uri(httpretty.POST, 'http://localhost:8080/accounts',
                               body=self._get_account_response)
        user_container = Container.generate('test')
        operator_container = Container.generate(self.client.secret)
        result = self.client.create_wallet4_account(self.id,
                                                    user_container=user_container,
                                                    operator_container=operator_container,
                                                    currency='BTC')
        self.assertIsInstance(result, Account)

    @httpretty.activate
    def test_create_account_simple(self):
        httpretty.register_uri(httpretty.POST, 'http://localhost:8080/accounts',
                               body=self._get_account_response)
        result = self.client.create_simple_account(self.id, currency='BTC')
        self.assertIsInstance(result, Account)

    @httpretty.activate
    def test_update_account_wallet4(self):
        httpretty.register_uri(httpretty.PUT, 'http://localhost:8080/accounts',
                               body=self._get_account_response)
        user_container = Container.generate('test')
        result = self.client.update_wallet4_account(self.id, user_container=user_container,
                                                    operator_container=Container.generate(self.client.secret),
                                                    currency='BTC')
        self.assertIsInstance(result, Account)

    @httpretty.activate
    def test_get_balance(self):
        url = 'http://localhost:8080/balances/BTC/{external_id}'.format(external_id=self.id)
        httpretty.register_uri(httpretty.GET, url,
                               body=json.dumps({u'address': u'38gP2E6Fj2s3sx63urYPpSrgTwupHGvKsK',
                                                u'balance': u'0.0011086',
                                                u'balanceInSatoshis': u'110860',
                                                u'currencySymbol': u'BTC'}))
        balance = self.client.get_balance(self.id, 'BTC')
        self.assertEqual(0.0011086, balance)

    @httpretty.activate
    def test_get_account(self):
        url = 'http://localhost:8080/accounts/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.GET, url, body=self._get_account_response)
        account = self.client.get_account(self.id, 'BTC')
        self.assertIsInstance(account, Account)

    @httpretty.activate
    def test_build_transaction(self):
        url = 'http://localhost:8080/transactions/build/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.POST, url, body=self._build_transaction_response)
        transaction = self.client.build_transaction(self.id, 'BTC', '39Ccf2Hr2ns58ugt1mRZw7tKA3AhZu41EJ', 0.00001)
        self.assertIsInstance(transaction, Wallet4Transaction)

    @httpretty.activate
    def test_cosign(self):
        url = 'http://localhost:8080/transactions/build/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.POST, url, body=self._build_transaction_response)
        url = 'http://localhost:8080/accounts/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.GET, url, body=self._get_account_response)

        transaction = self.client.build_transaction(self.id, 'BTC', '39Ccf2Hr2ns58ugt1mRZw7tKA3AhZu41EJ', 0.00001)
        transaction = self.client.sign_wallet4_transaction(transaction, self.id, 'BTC')
        self.assertIsInstance(transaction, Wallet4Transaction)

    @httpretty.activate
    def test_cosign_and_submit(self):
        url = 'http://localhost:8080/transactions/build/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.POST, url, body=self._build_transaction_response)
        url = 'http://localhost:8080/accounts/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.GET, url, body=self._get_account_response)
        url = 'http://localhost:8080/transactions/submit/{external_id}/BTC'.format(external_id=self.id)
        httpretty.register_uri(httpretty.POST, url, body=self._transaction_ok)

        transaction = self.client.build_transaction(self.id, 'BTC', '38EyoyyZC5tyvmhjNyT9YR3ZDoSesCYjPR', 0.00001)
        transaction = self.client.sign_wallet4_transaction(transaction, self.id, 'BTC')
        transaction = self.client.cosign_by_user('test', transaction, self.id, 'BTC')
        response = self.client.submit(self.id, transaction, 'BTC')
        self.assertEqual(response['state'], 'sending')


class CryptTestCase(unittest.TestCase):
    def test_encrypt(self):
        crypt = Crypt('test')
        with mock.patch('ambisafe.crypt.generate_iv') as generate_iv:
            generate_iv.return_value = 'ff55e03b11dc43adf839c3aee3632b36'.decode('hex')
            iv, data = crypt.encrypt('8a3167b6032285a9fd89fcf9110d51ce1cffaf0eb21bc316560d0e510ebac7cd',
                                     'ca20faef-ac3f-40a6-99c0-500855c03207')
        self.assertEqual(data, 'a0b0cbf2c2697f5141041da8a012149dc4cd82df6f43be8c'
                               'fc58342ba8e663722178509b667217f2c990ec24ffaeb2ed')

    def test_decrypt(self):
        crypt = Crypt('test')
        private_key = crypt.decrypt('a0b0cbf2c2697f5141041da8a012149dc4cd82df6f43be8c'
                                    'fc58342ba8e663722178509b667217f2c990ec24ffaeb2ed',
                                    'ca20faef-ac3f-40a6-99c0-500855c03207',
                                    'ff55e03b11dc43adf839c3aee3632b36')
        self.assertEqual(private_key, '8a3167b6032285a9fd89fcf9110d51ce1cffaf0eb21bc316560d0e510ebac7cd')

if __name__ == '__main__':
    unittest.main()
