import json
import platform
import requests

from . import __version__
from .compat import urljoin
from .encoder import SmartJSONEncoder
from .error import GatewayError, HttpError

__all__ = ('APIRequestor',)

# This dictionary is used to dynamically select the appropriate platform for
# the user agent string.
OS_VERSION_INFO = {
    'Linux': '%s' % (platform.linux_distribution()[0]),
    'Windows': '%s' % (platform.win32_ver()[0]),
    'Darwin': '%s' % (platform.mac_ver()[0]),
}

USER_AGENT = 'qualpay-python/{lib_ver} {py_impl}/{py_ver} {os}/{os_dist}'.format(
    lib_ver=__version__,
    py_impl=platform.python_implementation(),
    py_ver=platform.python_version(),
    os=platform.system(),
    os_dist=OS_VERSION_INFO.get(platform.system(), 'X')
)


class APIRequestor(object):
    def __init__(self, merchant_id=None, security_key=None, base_endpoint=None):
        self.merchant_id = merchant_id
        self.security_key = security_key
        self.base_endpoint = base_endpoint

    def request(self, endpoint, data):
        endpoint = urljoin(self.base_endpoint, endpoint)
        response = requests.post(
            url=endpoint,
            data=self.prepare_data(data),
            headers=self.get_headers(),
            timeout=10
        )

        if response.status_code != 200:
            raise HttpError(response.status_code, response)

        data = response.json()
        if not data['rcode'].startswith('0'):
            raise GatewayError(data['rcode'], response)

        return data

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT
        }

    def prepare_data(self, data):
        data.update({
            'merchant_id': self.merchant_id,
            'security_key': self.security_key,
        })
        return json.dumps(data, cls=SmartJSONEncoder)
