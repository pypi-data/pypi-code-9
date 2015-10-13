import pytest
import aplazame_sdk

from .base import PrivateTestCase


class ClientTestCase(PrivateTestCase):

    def test_delete(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.delete('/orders')

        self.assertEqual(excinfo.value.code, 405)

    def test_default_host(self):
        client = aplazame_sdk.Client(
            access_token=self.private_token, sandbox=True,
            version=self.api_version, verify=self.verify)

        self.assertEqual(client.host, 'api.aplazame.com')

    def test_exception_value_error(self):
        self.client.ctype = 'xml'

        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.order_detail('404')

        self.assertIsNone(excinfo.value.type)

    def test_error_repr(self):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.client.post('/orders')

        self.assertIn('not allowed', repr(excinfo.value))
