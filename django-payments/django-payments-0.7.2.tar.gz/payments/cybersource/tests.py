from __future__ import unicode_literals
import datetime
from decimal import Decimal
from unittest import TestCase

from . import CyberSourceProvider
from .. import PurchasedItem, RedirectNeeded

CLIENT_ID = 'abc123'
PAYMENT_TOKEN = '5a4dae68-2715-4b1e-8bb2-2c2dbe9255f6'
SECRET = '123abc'
VARIANT = 'wallet'


class Attrs(dict):
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    def __delattr__(self, item):
        del self[item]


class Payment(object):

    id = 1
    description = 'payment'
    currency = 'AED'
    delivery = Decimal(10)
    status = 'waiting'
    fraud_status = 'unknown'
    tax = Decimal(10)
    token = PAYMENT_TOKEN
    total = Decimal(210)
    variant = VARIANT
    transaction_id = None

    billing_first_name = 'John'
    billing_last_name = 'Doe'
    billing_address_1 = 'Somewhere'
    billing_address_2 = 'Over the Rainbow'
    billing_city = 'Washington'
    billing_country_code = 'US'
    billing_country_area = 'District of Columbia'
    billing_postcode = '20505'
    billing_email = 'test@room-303.com'

    customer_ip_address = '82.196.81.11'
    attrs = Attrs()

    def change_status(self, status, message='', commit=True):
        self.status = status

    def change_fraud_status(self, status, message='', commit=True):
        self.fraud_status = status

    def get_failure_url(self):
        return 'http://cancel.com'

    def get_process_url(self):
        return 'http://example.com'

    def get_purchased_items(self):
        return [
            PurchasedItem(
                name='foo', quantity=Decimal('10'), price=Decimal('20'),
                currency='AED', sku='bar')]

    def get_success_url(self):
        return 'http://success.com'


class TestCyberSourceProvider(TestCase):

    def test_purchase(self):
        payment = Payment()
        provider = CyberSourceProvider(
            capture=False,
            merchant_id='NI_MAGRUDY_AED',
            password='2DROk7NEWI2nrjKzG5LGjm1kMeN955MhVXFezc/1wzMi6tTmQyuSyxVWZveMlqi3PAuqIST+q9JQ4882JDH8b6xVlkMUmXGXdu7I4kfBeNNitAHmi7Kd4U5z9NPmzXExt+suXMTVI8rctpLP/cAv3qGQZVZSeVLBm/LET8I7W9/yi6NwPJV4pslSCVoFy5xu/Cjppeeh6d5rrK7HFioV3GKt15opCNwd9J/RC+Iw/ixQJ2qnVD4ELKQbwTaamzEYxxYH2ob4RIudESeGNURIIMRtopDeaLk8PgwpGG7sHC33g58e1UMe9cDQv55iO+ONWCHCsgLXzuerN5E6WEVBLQ==')
        # provider.refund()
        today = datetime.date.today()
        with self.assertRaises(RedirectNeeded):
            provider.get_form(payment, {
                'expiration_0': '12',
                'expiration_1': str(today.year),
                'name': 'Tester',
                'number': '4111111111111111',
                'cvv2': '123'})
