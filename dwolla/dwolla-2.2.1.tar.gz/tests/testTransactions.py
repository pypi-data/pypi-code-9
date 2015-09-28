import unittest

from dwolla import transactions, constants
from mock import MagicMock


class TransTest(unittest.TestCase):
    def setUp(self):
        transactions.r._get = MagicMock()
        transactions.r._post = MagicMock()
        transactions.r._put = MagicMock()
        transactions.r._delete = MagicMock()

        constants.client_id = "SOME ID"
        constants.client_secret = "SOME ID"
        constants.access_token = "AN OAUTH TOKEN"
        constants.pin = 1234

    def testsend(self):
        transactions.send('812-111-1234', 5.00, a='parameter')
        transactions.r._post.assert_any_call('/transactions/send', {'a': 'parameter', 'destinationId': '812-111-1234', 'oauth_token': 'AN OAUTH TOKEN', 'amount': 5.0, 'pin': 1234}, dwollaparse='dwolla')

    def testget(self):
        transactions.get(another='parameter')
        transactions.r._get.assert_any_call('/transactions', {'client_secret': 'SOME ID', 'oauth_token': 'AN OAUTH TOKEN', 'another': 'parameter', 'client_id': 'SOME ID'}, dwollaparse='dwolla')

    def testinfo(self):
        transactions.info('123456')
        transactions.r._get.assert_any_call('/transactions/123456', {'client_secret': 'SOME ID', 'oauth_token': 'AN OAUTH TOKEN', 'client_id': 'SOME ID'}, dwollaparse='dwolla')

    def testrefund(self):
        transactions.refund('12345', 'Balance', 10.50, a='parameter')
        transactions.r._post.assert_any_call('/transactions/refund', {'fundsSource': 'Balance', 'a': 'parameter', 'pin': 1234, 'amount': 10.5, 'oauth_token': 'AN OAUTH TOKEN', 'transactionId': '12345'}, dwollaparse='dwolla')

    def teststats(self):
        transactions.stats(a='parameter')
        transactions.r._get.assert_any_call('/transactions/stats', {'a': 'parameter', 'oauth_token': 'AN OAUTH TOKEN'}, dwollaparse='dwolla')

    def testschedule(self):
        transactions.schedule('812-111-1234', 5.00, '2018-01-01', 'abcdefunds', a='parameter')
        transactions.r._post.assert_any_call('/transactions/scheduled', {'a': 'parameter', 'destinationId': '812-111-1234', 'oauth_token': 'AN OAUTH TOKEN', 'amount': 5.0, 'scheduleDate': '2018-01-01', 'pin': 1234, 'fundsSource': 'abcdefunds'}, dwollaparse='dwolla')

    def testscheduled(self):
        transactions.scheduled()
        transactions.r._get.assert_any_call('/transactions/scheduled', {'oauth_token': 'AN OAUTH TOKEN'}, dwollaparse='dwolla')

    def testscheduledbyid(self):
        transactions.scheduledbyid('1234')
        transactions.r._get.assert_any_call('/transactions/scheduled/1234', {'oauth_token': 'AN OAUTH TOKEN'}, dwollaparse='dwolla')

    def testeditscheduledbyid(self):
        transactions.editscheduledbyid('1234', amount=5.5)
        transactions.r._put.assert_any_call('/transactions/scheduled/1234', {'oauth_token': 'AN OAUTH TOKEN', 'amount': 5.5, 'pin': 1234}, dwollaparse='dwolla')

    def testdeletescheduledbyid(self):
        transactions.deletescheduledbyid('1234')
        transactions.r._delete.assert_any_call('/transactions/scheduled/1234', {'oauth_token': 'AN OAUTH TOKEN', 'pin': 1234}, dwollaparse='dwolla')

    def testdeleteallscheduled(self):
        transactions.deleteallscheduled()
        transactions.r._delete.assert_any_call('/transactions/scheduled', {'oauth_token': 'AN OAUTH TOKEN', 'pin': 1234}, dwollaparse='dwolla')

if __name__ == '__main__':
    unittest.main()
