from .base import PrivateTestCase
from .decorators import instance_required


class MerchantsTestCase(PrivateTestCase):

    def setUp(self):
        super(MerchantsTestCase, self).setUp()

        results = self.client.merchants().json()['results']
        self.instance = results[0] if results else None

    def test_list(self):
        response = self.client.merchants()
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_detail(self):
        response = self.client.merchant_detail(self.instance['id'])
        self.assertEqual(response.status_code, 200)

    def test_me(self):
        response = self.client.me()
        self.assertEqual(response.status_code, 200)

    def test_operations(self):
        response = self.client.operations()
        self.assertEqual(response.status_code, 200)

    def test_payments(self):
        response = self.client.payments()
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_merchant_operations(self):
        response = self.client\
            .merchant_request('operations', self.instance['id'])
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_merchant_payments(self):
        response = self.client\
            .merchant_request('payments', self.instance['id'])
        self.assertEqual(response.status_code, 200)
