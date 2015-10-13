import random

from .base import PublicTestCase


class SimulatorTestCase(PublicTestCase):

    def test_get_simulator(self):
        response = self.client.simulator(amount=random.randint(1000, 10000))
        self.assertEqual(response.status_code, 200)
