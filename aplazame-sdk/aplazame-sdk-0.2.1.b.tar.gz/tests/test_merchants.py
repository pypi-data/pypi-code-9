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
