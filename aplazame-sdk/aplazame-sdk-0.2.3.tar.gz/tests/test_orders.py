import pytest
import aplazame_sdk

from .base import PrivateTestCase
from .decorators import instance_required


class OrdersTestCase(PrivateTestCase):

    def setUp(self):
        super(OrdersTestCase, self).setUp()

        response = self.client.orders({'ordering': '-cancelled,confirmed'})

        qs = response.json()['results']

        if qs and qs[0]['cancelled'] is None\
                and qs[0]['confirmed'] is not None:

            self.instance = qs[0]

        else:
            raise Exception('Test order not found')

    def test_list(self):
        response = self.client.orders()
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.orders(page=2)
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_detail(self):
        response = self.client.order_detail(self.instance['id'])
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_refund_check(self):
        response = self.client.refund_check(self.instance['mid'])
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_refund(self):
        response = self.client.refund(self.instance['mid'], amount=1)
        self.assertEqual(response.status_code, 200)

    @instance_required
    def test_authorize(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.authorize(self.instance['mid'])

        self.assertEqual(excinfo.value.code, 403)

    @instance_required
    def test_partial_update(self):
        response = self.client.update(self.instance['mid'], {
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

    def test_cancel(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.cancel('404')

        self.assertEqual(excinfo.value.code, 404)

    @instance_required
    def test_update(self):
        response = self.client.update(self.instance['mid'], {
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

    @instance_required
    def test_history(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.history(self.instance['mid'], {})

        self.assertEqual(excinfo.value.code, 403)
