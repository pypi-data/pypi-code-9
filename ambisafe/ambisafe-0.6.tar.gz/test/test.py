from functools import partial
import json
from random import randint, choice
import string
import unittest
import httpretty

from ambisafe import Account, Container, Wallet4Transaction, Client, Crypt, KEY_LENGTH


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
                            'cKey": "02b50294dcc261642ec45b11a30dedeb844565cebfb02cd9101fcca7ac38020016", "data": "ac' \
                            'a6851f8cd90d054871c393d16cffa00f4ea4c0ec6e29aee660bfaa131ea65099d820a65e361d1a35baeb477b' \
                            '37bbfd78f4d718fd5d661d36849e6b51ad9639d928aefe40a4c81936b091fd216801bc", "salt": "3d2b86' \
                            '9e-8a8f-4989-baa4-acc7d5e3d42c", "iv": "58d1b6c842e988ed7eab8613744a36c8"},"OPERATOR":{"' \
                            'publicKey": "02553c456dfa78695e8a1e5451c496c3021b45a4faee101457c5d3fa59caf4c49a", "data"' \
                            ': "2b670a9249679f901e08d75a6910083f0b691d42ea8fab00036f86d1b58f07377e8dffc8742c097d930e5' \
                            'a463e4045c84b0393f81ed27b26add7ea804c35a605ed15b9d5208bc99e3726375abad12e7f", "salt": "1' \
                            '3232665-d0f4-4c61-bf57-570105bae3ab", "iv": "4ab943077ce57502f81255b2e905dff1"}}}' % id
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
        cls.client = Client('http://localhost:8080', 'ololo', 'demo', 'demo')

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
        transaction = self.client.cosign_by_user('ololo', transaction, self.id, 'BTC')
        response = self.client.submit(self.id, transaction, 'BTC')
        self.assertEqual(response['state'], 'sending')


class CryptTestCase(unittest.TestCase):
    def _crypt(self, data, salt):
        crypt = Crypt('ololo')
        return crypt.encrypt(data, salt)

    def test_encrypt(self):
        iv, data = self._crypt('13', 'salt')
        self.assertEqual(len(iv), KEY_LENGTH)
        self.assertEqual(len(data) % 16, 0)

    def test_decrypt(self):
        iv, data = self._crypt('13', 'salt')
        crypt = Crypt('ololo')
        self.assertEqual(crypt.decrypt(data, 'salt', iv), '13')

        iv, data = self._crypt('t' * 16, 'salt')
        crypt = Crypt('ololo')
        self.assertEqual(crypt.decrypt(data, 'salt', iv), 't' * 16)

        iv, data = self._crypt('', 'salt')
        crypt = Crypt('ololo')
        self.assertEqual(crypt.decrypt(data, 'salt', iv), '')

        # test random data
        for _ in xrange(20):
            random_string = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(randint(0, 10000)))
            salt = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(randint(0, 100)))
            iv, data = self._crypt(random_string, salt)
            crypt = Crypt('ololo')
            self.assertEqual(crypt.decrypt(data, salt, iv), random_string)

if __name__ == '__main__':
    unittest.main()
