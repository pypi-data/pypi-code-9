from .base import SdkBaseTestCase


class MerchantsTestCase(SdkBaseTestCase):

    def setUp(self):
        super(MerchantsTestCase, self).setUp()

        results = self.client.merchants().json()['results']
        self.merchant = results[0] if results else None

    def _merchant_required(f):
        def wrapped(self, *args, **kwargs):
            if self.merchant is not None:
                return f(self, *args, **kwargs)
        return wrapped

    def test_list(self):
        response = self.client.merchants()
        self.assertEqual(response.status_code, 200)

    @_merchant_required
    def test_detail(self):
        response = self.client.merchant_detail(self.merchant['id'])
        self.assertEqual(response.status_code, 200)
