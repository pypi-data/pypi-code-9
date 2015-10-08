# stdlib
import json
import ssl
import logging

# requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

from shushuo import exceptions


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
    base_url = "https://api.shushuo.com"

    # self says it belongs to ShushuoApi/andOr is the object passed into ShushuoApi
    # __init__ create api object whenever ShushuoApi class is invoked
    def __init__(self, project_id, write_key=None, read_key=None,
                 base_url=None, get_timeout=None, post_timeout=None,
                 master_key=None):
        """
        Initializes a ShushuoApi object

        :param project_id: the Shushuo project ID
        :param write_key: a Shushuo IO Scoped Key for Writes
        :param read_key: a Shushuo IO Scoped Key for Reads
        :param base_url: optional, set this to override where API requests
        are sent
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

        url = "{0}/events/{1}/".format(self.base_url, event.event_collection)
        headers = {
            "Content-Type": "application/json",
            "X-Project-Id": self.project_id,
            "X-Project-Key": self.write_key,
        }
        payload = json.dumps([event.to_json()])
        logging.info(payload)
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

        url = "{0}/events/".format(self.base_url)
        headers = {
            "Content-Type": "application/json",
            "X-Project-Id": self.project_id,
            "X-Project-Key": self.write_key,
        }
        payload = json.dumps(events)
        response = self.fulfill(HTTPMethods.POST, url, data=payload, headers=headers, timeout=self.post_timeout)
        self.error_handling(response)

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
