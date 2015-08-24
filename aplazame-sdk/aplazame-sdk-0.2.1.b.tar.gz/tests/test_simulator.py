import random

from .base import PublicTestCase


class SimulatorTestCase(PublicTestCase):

    def test_get_simulator(self):
        response = self.client.simulator(amount=random.randint(100, 1000))
        self.assertEqual(response.status_code, 200)
