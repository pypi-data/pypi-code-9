import pytest
import unittest
import aplazame_sdk


@pytest.mark.usefixtures('conf_class')
class SdkBaseTestCase(unittest.TestCase):

    def setUp(self):
        if self.private_token is None:
            raise Exception('Todo: mocks')

        self.client = aplazame_sdk.Client(
            access_token=self.private_token, host=self.host, sandbox=True,
            version=self.api_version, verify=self.verify)

    def tearDown(self):
        pass

    def request(self, method, action, *args, **kwargs):
        return getattr(self.client, method.lower())(action, *args, **kwargs)

    def requestError(self, method, action, *args, **kwargs):
        with pytest.raises(aplazame_sdk.AplazameError) as excinfo:
            self.request(method, action, *args, **kwargs)
        return excinfo.value

    def assertFieldError(self, error, field):
        self.assertIn(field, error.response.json()['error']['fields'])
