from calendar import timegm
from datetime import datetime, date, time
import json
from requests import Session
from six import iteritems
from six.moves.urllib.parse import urljoin
from . import api
from .exc import APIError
from .util import PagedResult


class Client(object):
    def __init__(self, url, username=None, password=None, cert=None, verify=False, _system_init=True):
        """Open a connection to a Security Center instance.

        Provides the interface for making raw requests to the API.  Modules are registered on the
        connection object for performing actions in an easier format.

        If a username and password are provided, they will be used to log in after connecting.

        SSL is possible by passing a client certificate and a trust chain.
        When using two-way SSL with a client certificate, ``system.init`` can cause an automatic
        log in if the certificate is registered.
        This can be disabled by setting ``_system_init`` to False.

        :param url: connect to a Security Center instance at this location. Must include scheme (https) and can include port (:443).
        :param username: after connecting, log in as this user, if given
        :param password: used for log in with username
        :param cert: path to client certificate for two-way SSL.  Can be a tuple of (cert, key) if they are separate.
        :param verify: how to verify host SSL cert.  If True, use system trust; if False, don't verify; otherwise, a path to a trust chain file.
        :param _system_init: whether to call ``system.init`` on connect
        """

        # true endpoint is "request.php"
        self._url = urljoin(url, 'request.php')

        # set up session with SSL
        self._session = Session()
        self._session.cert = cert
        self._session.verify = verify

        # token returned after login
        self._token = None

        self.asset = api.Asset(self)
        self.admin = api.Admin(self)
        self.auth = api.Auth(self)
        self.credential = api.Credential(self)
        self.file = api.File(self)
        self.heartbeat = api.Heartbeat(self)
        self.message = api.Message(self)
        self.nessus_result = api.NessusResult(self)
        self.plugin = api.Plugin(self)
        self.scan = api.Scan(self)
        self.scan_result = api.ScanResult(self)
        self.system = api.System(self)
        self.user = api.User(self)
        self.user_prefs = api.UserPrefs(self)
        self.vuln = api.Vuln(self)

        # try automatic login by client cert
        if _system_init:
            self.system.init()

        # try manual login by username
        if username is not None and password is not None:
            self.auth.login(username, password)

    @staticmethod
    def _process_input(input):
        """Serialize types to SC expected formats.

        - strip None values
        - bool becomes string 'true' or 'false'
        - datetime and date becomes timestamp

        :param input: input to process
        :return: new dict with processed input
        """

        if input is None:
            return {}

        processed_input = {}

        for key, value in iteritems(input):
            if value is None:
                continue

            if isinstance(value, bool):
                # why does the server expect strings instead of bools?
                value = str(value).lower()
            elif isinstance(value, datetime):
                value = timegm(value.utctimetuple())
            elif isinstance(value, date):
                value = timegm(datetime.combine(value, time()))

            processed_input[key] = value

        return processed_input


    def _request(self, module, action, input=None, file=None, parse=True, page_class=PagedResult):
        """Make an API call to the given api::action.

        :param module: name of api on server
        :param action: name of action in api
        :param input: any arguments to be passed to the api::action
        :param file: file data to upload
        :param parse: if False, return the raw response
        :param page_class: class to use for pagination if possible, default :class:`PagedResult`
        :return: dict containing API response, or ``Response`` if parse is False
        """

        input = self._process_input(input)
        r = self._session.post(self._url, {
            'module': module,
            'action': action,
            'request_id': 0,
            'token': self._token,
            'input': json.dumps(input)
        }, files={'Filedata': file} if file else None)
        r.raise_for_status()

        if not parse:
            return r

        data = r.json()
        code = data.get('error_code')

        if code:
            message = data['error_msg']
            raise APIError(code, message)

        data = data['response']

        if page_class and page_class._can_page(data):
            page_class(self, module, action, input, data)

        return data
