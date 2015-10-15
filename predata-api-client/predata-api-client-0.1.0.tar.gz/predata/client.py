import requests
import bs4

from helpers.signal_client import PredataSignalClient
from helpers.data_client import PredataDataClient
from helpers.analysis_client import PredataAnalysisClient
from helpers.system_client import PredataSystemClient

from config.constants import PRODUCTION_HOSTNAME, DEVELOPMENT_HOSTNAME, API_BASE_VERSION_1
from config.exceptions import PredataPythonClientExeception


class PredataClient():

    """
    Predata Python API Client.
    """

    data_client = None
    signal_client = None
    analysis_client = None
    system_client = None

    def __init__(self, token=None, username=None, password=None, version=1, hostname="prod"):
        """
        Supports token authentication or basic authentication.
        """
        if version == 1:
            self.API_BASE = API_BASE_VERSION_1
        else:
            raise PredataPythonClientExeception("Unsupported API version")

        if hostname == "prod":
            self.HOSTNAME = PRODUCTION_HOSTNAME
        elif hostname == "dev":
            self.HOSTNAME = DEVELOPMENT_HOSTNAME  # note: only Predata staff users will be able to access
        else:
            raise PredataPythonClientExeception("Unsupported Host: %s" % hostname)

        if not token and not (username and password):
            raise PredataPythonClientExeception("No authentication credentials provided")

        self.session = requests.Session()

        if token:
            self._token_auth(token)
        elif (username and password):
            self._basic_auth(username, password)

    def _token_auth(self, token):
        """
        Add token authentication to session
        """
        self.session.headers.update({"Authorization": "Token %s" % token})

    def _basic_auth(self, username, password):
        """
        Add basic authentication cookies to session
        """
        login_url = self.HOSTNAME + "/users/sign_in/"
        r = self.session.get(login_url)
        soup = bs4.BeautifulSoup(r.text)
        token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})["value"]
        auth = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": token,
        }
        r = self.session.post(login_url, data=auth, headers={"Referer": login_url})

    def signals(self):
        """
        Access signals client.
        """
        if not self.signal_client:
            self.signal_client = PredataSignalClient(self.session, self.HOSTNAME, self.API_BASE)
        return self.signal_client

    def data(self):
        """
        Access data client.
        """
        if not self.data_client:
            self.data_client = PredataDataClient(self.session, self.HOSTNAME, self.API_BASE)
        return self.data_client

    def analysis(self):
        """
        Access analysis client.
        """
        if not self.analysis_client:
            self.analysis_client = PredataAnalysisClient(self.session, self.HOSTNAME, self.API_BASE)
        return self.analysis_client

    def system(self):
        """
        Access system client.
        """
        if not self.system_client:
            self.system_client = PredataSystemClient(self.session, self.HOSTNAME, self.API_BASE)
        return self.system_client
