from .base import SdkBaseTestCase


class CustomersTestCase(SdkBaseTestCase):

    def setUp(self):
        super(CustomersTestCase, self).setUp()

        results = self.client.customers().json()['results']
        self.customer = results[0] if results else None

    def _customer_required(f):
        def wrapped(self, *args, **kwargs):
            if self.customer is not None:
                return f(self, *args, **kwargs)
        return wrapped

    def test_list(self):
        response = self.client.customers()
        self.assertEqual(response.status_code, 200)

    @_customer_required
    def test_detail(self):
        response = self.client.customer_detail(self.customer['id'])
        self.assertEqual(response.status_code, 200)

    @_customer_required
    def _test_history(self):
        response = self.client.customer_history(self.customer['id'])
        self.assertEqual(response.status_code, 200)
