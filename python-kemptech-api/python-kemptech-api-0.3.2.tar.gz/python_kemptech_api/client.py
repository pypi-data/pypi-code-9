import abc
from past.builtins import long

import logging
import requests
from requests import exceptions
import six

from .util import ApiXmlHelper
from .exceptions import KempTechApiException, CommandNotAvailableException


requests.packages.urllib3.disable_warnings()
log = logging.getLogger(__name__)


class HttpClient(object):
    """Client that performs HTTP requests."""

    endpoint = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def _do_request(self, http_method, rest_command,
                    parameters=None,
                    file=None):
        """Perform a HTTP request.

        :param http_method: GET or POST.
        :param rest_command: The command to run.
        :param parameters: dict containing parameters.
        :param file: Location of file to send.
        :return: The Status code of request and the response text body.
        """
        cmd_url = "{endpoint}{cmd}?".format(endpoint=self.endpoint,
                                            cmd=rest_command)
        log.debug("Request is: %s", cmd_url)

        try:
            if file is not None:
                with open(file, 'rb') as payload:
                    response = requests.request(http_method, cmd_url,
                                                params=parameters,
                                                verify=False,
                                                data=payload)
            else:
                response = requests.request(http_method, cmd_url,
                                            params=parameters,
                                            verify=False)
            if 400 < response.status_code < 500:
                raise KempTechApiException(code=response.status_code)
            else:
                response.raise_for_status()
        except exceptions.ConnectionError:
            log.exception("A connection error occurred to %s.", self.endpoint)
            raise
        except exceptions.URLRequired:
            log.exception("%s is an invalid URL", cmd_url)
            raise
        except exceptions.TooManyRedirects:
            log.exception("Too many redirects with request to %s.", cmd_url)
            raise
        except exceptions.Timeout:
            log.exception("A connection %s has timed out.", self.endpoint)
            raise
        except exceptions.HTTPError:
            log.exception("A HTTP error occurred with request to %s.", cmd_url)
            raise KempTechApiException(msg=response.text)
        except exceptions.RequestException:
            log.exception("An error occurred with request to %s.", cmd_url)
            raise
        return response.text

    def _get(self, rest_command, parameters=None):
        return self._do_request('GET', rest_command, parameters)

    def _post(self, rest_command, file=None):
        return self._do_request('POST', rest_command, file=file)


class ComplexIdMixin(object):
    """Mixin for adding non-trivial IDs."""

    @abc.abstractproperty
    def id(self):
        """Must return a dict with unique ID parameters for KEMP API."""
        raise NotImplementedError("This abstractproperty needs implementation")

    @id.setter
    @abc.abstractmethod
    def id(self, value):
        raise NotImplementedError("This abstractmethod needs implementation")


class BaseObjectModel(HttpClient):
    """A class to build objects based on KEMP RESTful API.

    Subclasses built from this class need to name their parameters
    the same as their RESTful API counterpart in order for this
    class to work.
    """

    @abc.abstractproperty
    def api_name(self):
        raise NotImplementedError("This abstractproperty needs implementation")

    def __init__(self, parameters):
        for api_key, api_value in parameters:
            self.__dict__[api_key] = api_value

    def save(self):
        command = 'mod' if self.exists else 'add'
        self._get_request('%s%s' % (command, self.api_name), self.to_dict())

    def delete(self):
        self._get_request('%s%s' % ('del', self.api_name), self.id)

    @property
    def exists(self):
        return self._get_request('show' + self.api_name, self.id) < 300

    def to_dict(self):
        """Return a dictionary containing attributes of class.

        Ignore attributes that are set to None or are not a string or int;
        also ignore endpoint as it is not an API thing.
        """
        attributes = {}
        for attr in self.__dict__:
            if (self.__dict__[attr] is not None or not
                    self.__dict__[attr] == 'endpoint' or not
                    isinstance(self.__dict__[attr], six.string_types) or not
                    isinstance(self.__dict__[attr], (int, long))):
                attributes[attr] = self.__dict__[attr]
        return attributes


class LoadMaster(HttpClient):
    """LoadMaster API object."""

    def __init__(self, ip, username, password):
        self.ip_address = ip
        self.username = username
        self.password = password

    @property
    def endpoint(self):
        return "https://{user}:{pw}@{ip}/access".format(user=self.username,
                                                         pw=self.password,
                                                         ip=self.ip_address)

    def set_parameter(self, parameter, value):
        parameters = {
            'param': parameter,
            'value': value,
        }
        response = self._get('/set', parameters)
        return ApiXmlHelper.is_successful(response)

    def get_parameter(self, parameter):
        parameters = {
            'param': parameter,
        }
        response = self._get('/get', parameters)
        value = ApiXmlHelper.get_data_field(response, parameter)
        if isinstance(value, dict):
            # This hack converts possible HTML to an awful one string
            # disaster instead of returning parsed html as an OrderedDict.
            value = "".join("{!s}={!r}".format(key, val) for (key, val) in
                            value.items())
        return value

    def enable_api(self):
        """Enable LoadMaster API"""
        # Can't use the HttpClient methods for this as the
        # endpoint is different when attempting to enable the API.
        url = ("https://{user}:{pw}@{ip}"
               "/progs/doconfig/enableapi/set/yes/").format(user=self.username,
                                                            pw=self.password,
                                                            ip=self.ip_address)
        try:
            response = requests.get(url, verify=False)
        except exceptions.RequestException:
            log.exception("An unknown error occurred with request to %s",
                          url)
            raise KempTechApiException(response.text)

    def stats(self):
        response = self._get('/stats')
        if ApiXmlHelper.is_successful(response):
            return ApiXmlHelper.parse_to_dict(response)
        else:
            raise KempTechApiException(ApiXmlHelper.get_error_msg(response))

    def update_firmware(self, file):
        response = self._post('/installpatch', file)
        return ApiXmlHelper.is_successful(response)

    def shutdown(self):
        response = self._get('/shutdown')
        return ApiXmlHelper.is_successful(response)

    def reboot(self):
        response = self._get('/reboot')
        return ApiXmlHelper.is_successful(response)

    def get_sdn_controller(self):
        response = self._get('/getsdncontroller')
        if ApiXmlHelper.is_successful(response):
            return ApiXmlHelper.parse_to_dict(response)
        else:
            raise KempTechApiException(ApiXmlHelper.get_error_msg(response))

    def get_license_info(self):
        try:
            response = self._get('360/licenseinfo')
            if ApiXmlHelper.is_successful(response):
                return ApiXmlHelper.parse_to_dict(response)
            else:
                raise KempTechApiException(ApiXmlHelper.get_error_msg(response))
        except KempTechApiException:
            raise CommandNotAvailableException('/access360/licenseinfo')

    def list_addons(self):
        response = self._get('/listaddon')
        if ApiXmlHelper.is_successful(response):
            return ApiXmlHelper.parse_to_dict(response)
        else:
            raise KempTechApiException(ApiXmlHelper.get_error_msg(response))
