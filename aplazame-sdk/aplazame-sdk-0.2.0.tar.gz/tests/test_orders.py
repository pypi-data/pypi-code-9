import pytest
import aplazame_sdk

from .base import SdkBaseTestCase


class OrdersTestCase(SdkBaseTestCase):

    def setUp(self):
        super(OrdersTestCase, self).setUp()

        response = self.client.orders({
            'ordering': '-cancelled,confirmed'
        })

        qs = response.json()['results']

        if qs and qs[0]['cancelled'] is None\
                and qs[0]['confirmed'] is not None:

            self.order = qs[0]

        else:
            self.order = None

    def _order_required(f):
        def wrapped(self, *args, **kwargs):
            if self.order is not None:
                return f(self, *args, **kwargs)
        return wrapped

    def test_list(self):
        response = self.client.orders()
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.orders(page=2)
        self.assertEqual(response.status_code, 200)

    @_order_required
    def test_detail(self):
        response = self.client.order_detail(self.order['id'])
        self.assertEqual(response.status_code, 200)

    @_order_required
    def test_refund_check(self):
        response = self.client.refund_check(self.order['mid'])
        self.assertEqual(response.status_code, 200)

    @_order_required
    def test_refund(self):
        response = self.client.refund(self.order['mid'], amount=1)
        self.assertEqual(response.status_code, 200)

    @_order_required
    def test_authorize(self):
        response = self.client.authorize(self.order['mid'])
        self.assertEqual(response.status_code, 200)

    @_order_required
    def test_partial_update(self):
        response = self.client.update(self.order['mid'], {
            'order': {
                'articles': [{
                    'id': '59825349042875546873',
                    'name': 'N5 eau premiere spray',
                    'description': 'A decidedly lighter, fresher...',
                    'url': 'http://www.chanel.com',
                    'image_url': 'http://www.chanel.com',
                    'quantity': 1,
                    'price': 29000,
                    'tax_rate': 2100
                }],
                'discount': 300
            }
        }, partial=True)

        self.assertEqual(response.status_code, 204)

    @_order_required
    def test_cancel(self):
        order = self.client.orders({
            'ordering': 'cancelled,confirmed'
        }).json()['results'][0]

        if order['cancelled'] is not None:
            with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
                self.client.cancel(order['mid'])

            self.assertEqual(excinfo.value.code, 403)

        else:
            response = self.client.cancel(order['mid'])
            self.assertEqual(response.status_code, 204)

    @_order_required
    def test_update(self):
        response = self.client.update(self.order['mid'], {
            'order': {
                'shipping': {
                    'first_name': 'Hobbes',
                    'last_name': 'Watterson',
                    'phone': '616123456',
                    'alt_phone': '+34917909930',
                    'street': 'Calle del Postigo de San Martin 8',
                    'address_addition': 'Cerca de la plaza Santa Ana',
                    'city': 'Madrid',
                    'state': 'Madrid',
                    'country': 'ES',
                    'zip': '28013',
                    'price': 500,
                    'tax_rate': 2100,
                    'name': 'Planet Express',
                    'discount': 100
                },
                'articles': [{
                    'id': '59825349042875546873',
                    'name': 'N5 eau premiere spray',
                    'description': 'A decidedly lighter, fresher...',
                    'url': 'http://www.chanel.com',
                    'image_url': 'http://www.chanel.com',
                    'quantity': 1,
                    'price': 29000,
                    'tax_rate': 2100
                }],
                'discount': 300,
                'currency': 'EUR',
                'total_amount': 31080
            }
        })

        self.assertEqual(response.status_code, 204)

    @_order_required
    def test_history(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.history(self.order['mid'], {})

        self.assertEqual(excinfo.value.code, 403)
