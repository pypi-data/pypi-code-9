import requests

from django.test import TestCase, RequestFactory
from dps.transactions import make_payment

from .models import Payment


class DpsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_interactive(self):
        amount = 112.45
        payment = Payment.objects.create(amount=amount)

        request = self.factory.get('/', HTTP_HOST='localhost:8000')
        response = make_payment(payment, request=request)
        self.assertEqual(response.status_code, 302)
        response = requests.get(response['Location'])

        # check the dps page looks approximately correct
        self.assertIn('Payment Checkout', response.content)
        self.assertIn(str(amount), response.content)

    def test_recurring(self):
        pass
