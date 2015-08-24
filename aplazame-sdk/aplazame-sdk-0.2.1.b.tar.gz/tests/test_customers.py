from .base import PrivateTestCase
from .decorators import instance_required


class CustomersTestCase(PrivateTestCase):

    def setUp(self):
        super(CustomersTestCase, self).setUp()

        results = self.client.customers().json()['results']
        self.instance = results[0] if results else None

    def test_list(self):
        response = self.client.customers()
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_detail(self):
        response = self.client.customer_detail(self.instance['id'])
        self.assertEqual(response.status_code, 200)

    @instance_required
    def _test_history(self):
        response = self.client.customer_history(self.instance['id'])
        self.assertEqual(response.status_code, 200)
