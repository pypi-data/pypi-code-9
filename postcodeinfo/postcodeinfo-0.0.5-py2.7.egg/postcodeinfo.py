# -*- coding: utf-8 -*-
"""
A Python client library for the MOJ Postcode Info API.

Usage:

    >>> import postcodeinfo
    >>> client = postcodeinfo.Client('YOUR-API-TOKEN')
    >>> postcode = client.lookup_postcode('sw1a1aa')
    >>> postcode.valid
    True
    >>> postcode.addresses
    [
        {
            "uprn": "10033544614",
            "organisation_name": "BUCKINGHAM PALACE",
            "department_name": "",
            "po_box_number": "",
            "building_name": "",
            "sub_building_name": "",
            "building_number": null,
            "thoroughfare_name": "",
            "dependent_thoroughfare_name": "",
            "dependent_locality": "",
            "double_dependent_locality": "",
            "post_town": "LONDON",
            "postcode": "SW1A 1AA",
            "postcode_type": "L",
            "formatted_address": "Buckingham Palace\\nLondon\\nSW1A 1AA",
            "point": {
                "type":
                "Point",
                "coordinates": [
                    -0.141587558526369,
                    51.50100893654096
                ]
            }
        }
    ]
    >>> postcode.latitude
    51.50100893654096
    >>> postcode.longitude
    -0.141587558526369
    >>> postcode.local_authority
    {
        "name": "Westminster",
        "gss_code": "E09000033"
    }
"""

import os
import re
import urllib

import requests


__version__ = '0.0.5'

DEFAULT_TIMEOUT = 5

LONGITUDE = 0
LATITUDE = 1

DEFAULT_ADDRESS_FIELDS = (
    'uprn', 'organisation_name', 'department_name', 'po_box_number',
    'building_name', 'sub_building_name', 'building_number',
    'thoroughfare_name', 'dependent_thoroughfare_name', 'dependent_locality',
    'double_dependent_locality', 'post_town', 'postcode', 'postcode_type',
    'formatted_address', 'point')

NORMALISE = re.compile(r'[^a-z0-9]')


class PostcodeInfoException(Exception):
    pass


class NoResults(PostcodeInfoException):
    pass


class ServiceUnavailable(PostcodeInfoException):
    pass


class ServerException(PostcodeInfoException):
    pass


class Postcode(object):
    """
    Represents the info for a specified postcode.
    """

    info_path = 'postcodes/{postcode}/'

    def __init__(self, postcode, client):
        """
        Prepare a request for info on the specified postcode.

        :param postcode: The postcode to look up.
        :param client: The client instance.
        """
        self.as_given = postcode
        self._client = client

    @property
    def normalised(self):
        """
        The normalised postcode.
        """
        return re.sub(NORMALISE, '', self.as_given.lower())

    @property
    def _info(self):
        if getattr(self, '_postcodeinfo', None) is None:
            self._postcodeinfo = self._client._query_api(
                self.info_path.format(postcode=self.normalised))
        return self._postcodeinfo

    @property
    def valid(self):
        """
        ``True`` if the requested postcode is valid.
        """
        try:
            return self._info is not None
        except NoResults:
            return False

    @property
    def addresses(self, fields=None):
        """
        List of addresses associated with the postcode.
        Addresses are dict objects which look like the following::

            {
                "uprn": "10033544614",
                "organisation_name": "BUCKINGHAM PALACE",
                "department_name": "",
                "po_box_number": "",
                "building_name": "",
                "sub_building_name": "",
                "building_number": null,
                "thoroughfare_name": "",
                "dependent_thoroughfare_name": "",
                "dependent_locality": "",
                "double_dependent_locality": "",
                "post_town": "LONDON",
                "postcode": "SW1A 1AA",
                "postcode_type": "L",
                "formatted_address": "Buckingham Palace\\nLondon\\nSW1A 1AA",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.141587558526369,
                        51.50100893654096
                    ]
                }
            }
        """

        if fields is None:
            fields = ','.join(DEFAULT_ADDRESS_FIELDS)

        if getattr(self, '_addresses', None) is None:
            self._addresses = self._client._query_api(
                'addresses/',
                postcode=self.normalised,
                fields=fields)
        return self._addresses

    @property
    def latitude(self):
        """
        The latitude of the centre of the postcode area in degrees.
        """
        return self._info['centre']['coordinates'][LATITUDE]

    @property
    def longitude(self):
        """
        The longitude of the centre of the postcode area in degrees.
        """
        return self._info['centre']['coordinates'][LONGITUDE]

    @property
    def local_authority(self):
        """
        The local authority info for the postcode.
        """
        return self._info['local_authority']


class PartialPostcode(Postcode):
    """
    Represents the info for a specified partial postcode.
    """

    info_path = 'postcodes/partial/{postcode}/'


class Client(object):
    """
    Responsible for the API communication.
    """

    #: Default API URLs by environment
    api_urls = {
        'development': 'http://localhost:8000',
        'test': 'http://localhost:8000',
        'staging': 'https://postcodeinfo-staging.dsd.io',
        'production': 'https://postcodeinfo.service.gov.uk'
    }

    def __init__(self, auth_token=None, **kwargs):
        """
        Initialize a client instance.

        :param auth_token: Your authorization token for the API.
        :param api_url: The base URL of the API.
        :param timeout: Request timeout in seconds.
        :param env: ``development``, ``test``, ``staging`` or ``production`` -
            used to select a default ``api_url``
        """
        api_url = kwargs.get('api_url')
        env = kwargs.get('env')
        timeout = kwargs.get('timeout')
        self.timeout = DEFAULT_TIMEOUT
        self.url = api_url
        if api_url is None:
            if env is None:
                conf = self._conf_from_django_settings()
                if conf is not None:
                    self.url = conf['api_url']
                    self.token = conf['auth_token']
                    if conf['timeout'] is not None:
                        self.timeout = conf['timeout']
            if self.url is None:
                self.url = self._get_api_url(env)
        if auth_token is not None:
            self.token = auth_token
        if timeout is not None:
            self.timeout = timeout

    def lookup_postcode(self, postcode):
        """
        Request the postcode info from the API for the specified postcode.
        """
        return Postcode(postcode, self)

    def lookup_partial_postcode(self, partial_postcode):
        """
        Request the postcode info for the specified partial postcode.
        """
        return PartialPostcode(partial_postcode, self)

    def _query_api(self, endpoint, **kwargs):
        """
        Query the API.
        """
        try:
            response = requests.get(
                '{api}/{endpoint}?{args}'.format(
                    api=self.url,
                    endpoint=endpoint,
                    args=urllib.urlencode(kwargs)),
                headers={
                    'Authorization': 'Token {token}'.format(token=self.token)},
                timeout=self.timeout)

        except requests.RequestException as err:
            raise ServiceUnavailable(err)

        if response.status_code == 404:
            raise NoResults()

        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            raise ServerException(http_err)

        return response.json()

    def _conf_from_django_settings(self):
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            try:
                from django.conf import settings

                def get(name):
                    return getattr(settings, name, None)

                return {
                    'api_url': get('POSTCODEINFO_API_URL'),
                    'auth_token': get('POSTCODEINFO_AUTH_TOKEN'),
                    'timeout': get('POSTCODEINFO_TIMEOUT')}

            except ImportError:
                pass

    def _get_api_url(self, env=None):
        return self.api_urls.get(env, self.api_urls['development'])
