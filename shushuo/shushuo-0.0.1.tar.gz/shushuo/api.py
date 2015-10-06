# stdlib
import json
import ssl

# requests
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

# keen exceptions
from keen import exceptions

# json
from requests.compat import json


__author__ = 'dkador'


class HTTPMethods(object):

    """ HTTP methods that can be used with Shushuo's API. """

    GET = 'get'
    POST = 'post'
    DELETE = 'delete'


class ShushuoAdapter(HTTPAdapter):

    """ Adapt :py:mod:`requests` to Shushuo IO. """

    def init_poolmanager(self, connections, maxsize, block=False):

        """ Initialize pool manager with forced TLSv1 support. """

        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


class ShushuoApi(object):
    """
    Responsible for communicating with the Shushuo API. Used by multiple
    persistence strategies or async processing.
    """

    # the default base URL of the Shushuo API
    base_url = "https://api.keen.io"
    # the default version of the Shushuo API
    api_version = "3.0"

    # self says it belongs to ShushuoApi/andOr is the object passed into ShushuoApi
    # __init__ create keenapi object whenever ShushuoApi class is invoked
    def __init__(self, project_id, write_key=None, read_key=None,
                 base_url=None, api_version=None, get_timeout=None, post_timeout=None,
                 master_key=None):
        """
        Initializes a ShushuoApi object

        :param project_id: the Shushuo project ID
        :param write_key: a Shushuo IO Scoped Key for Writes
        :param read_key: a Shushuo IO Scoped Key for Reads
        :param base_url: optional, set this to override where API requests
        are sent
        :param api_version: string, optional, set this to override what API
        version is used
        :param get_timeout: optional, the timeout on GET requests
        :param post_timeout: optional, the timeout on POST requests
        :param master_key: a Shushuo IO Master API Key, needed for deletes
        """
        # super? recreates the object with values passed into ShushuoApi
        super(ShushuoApi, self).__init__()
        self.project_id = project_id
        self.write_key = write_key
        self.read_key = read_key
        self.master_key = master_key
        if base_url:
            self.base_url = base_url
        if api_version:
            self.api_version = api_version
        self.get_timeout = get_timeout
        self.post_timeout = post_timeout
        self.session = self._create_session()

    def _create_session(self):

        """ Build a session that uses ShushuoAdapter for SSL """

        s = requests.Session()
        s.mount('https://', ShushuoAdapter())
        return s

    def fulfill(self, method, *args, **kwargs):

        """ Fulfill an HTTP request to Shushuo's API. """

        return getattr(self.session, method)(*args, **kwargs)

    def post_event(self, event):
        """
        Posts a single event to the Shushuo IO API. The write key must be set first.

        :param event: an Event to upload
        """
        if not self.write_key:
            raise exceptions.InvalidEnvironmentError(
                "The Shushuo IO API requires a write key to send events. "
                "Please set a 'write_key' when initializing the "
                "ShushuoApi object."
            )

        url = "{0}/{1}/projects/{2}/events/{3}".format(self.base_url, self.api_version,
                                                       self.project_id,
                                                       event.event_collection)
        headers = {"Content-Type": "application/json", "Authorization": self.write_key}
        payload = event.to_json()
        response = self.fulfill(HTTPMethods.POST, url, data=payload, headers=headers, timeout=self.post_timeout)
        self.error_handling(response)

    def post_events(self, events):

        """
        Posts a single event to the Shushuo IO API. The write key must be set first.

        :param events: an Event to upload
        """
        if not self.write_key:
            raise exceptions.InvalidEnvironmentError(
                "The Shushuo IO API requires a write key to send events. "
                "Please set a 'write_key' when initializing the "
                "ShushuoApi object."
            )

        url = "{0}/{1}/projects/{2}/events".format(self.base_url, self.api_version,
                                                   self.project_id)
        headers = {"Content-Type": "application/json", "Authorization": self.write_key}
        payload = json.dumps(events)
        response = self.fulfill(HTTPMethods.POST, url, data=payload, headers=headers, timeout=self.post_timeout)
        self.error_handling(response)

    def query(self, analysis_type, params, all_keys=False):
        """
        Performs a query using the Shushuo IO analysis API.  A read key must be set first.

        """
        if not self.read_key:
            raise exceptions.InvalidEnvironmentError(
                "The Shushuo IO API requires a read key to perform queries. "
                "Please set a 'read_key' when initializing the "
                "ShushuoApi object."
            )

        url = "{0}/{1}/projects/{2}/queries/{3}".format(self.base_url, self.api_version,
                                                        self.project_id, analysis_type)

        headers = {"Authorization": self.read_key}
        payload = params
        response = self.fulfill(HTTPMethods.GET, url, params=payload, headers=headers, timeout=self.get_timeout)
        self.error_handling(response)

        response = response.json()

        if not all_keys:
            response = response["result"]

        return response

    def delete_events(self, event_collection, params):
        """
        Deletes events via the Shushuo IO API. A master key must be set first.

        :param event_collection: string, the event collection from which event are being deleted

        """
        if not self.master_key:
            raise exceptions.InvalidEnvironmentError(
                "The Shushuo IO API requires a master key to run deletes. "
                "Please set a 'master_key' when initializing the ShushuoApi object."
            )

        url = "{0}/{1}/projects/{2}/events/{3}".format(self.base_url,
                                                       self.api_version,
                                                       self.project_id,
                                                       event_collection)
        headers = {"Content-Type": "application/json", "Authorization": self.master_key}
        response = self.fulfill(HTTPMethods.DELETE, url, params=params, headers=headers, timeout=self.post_timeout)

        self.error_handling(response)
        return True

    def error_handling(self, res):
        """
        Helper function to do the error handling

        :params res: the response from a request
        """
        # making the error handling generic so if an status_code starting with 2 doesn't exist, we raise the error
        if res.status_code // 100 != 2:
            try:
                error = res.json()
            except json.JSONDecodeError:
                error = {
                    'message': 'The API did not respond with JSON, but: "{0}"'.format(res.text[:1000]),
                    "error_code": "InvalidResponseFormat"
                }
            raise exceptions.ShushuoApiError(error)
