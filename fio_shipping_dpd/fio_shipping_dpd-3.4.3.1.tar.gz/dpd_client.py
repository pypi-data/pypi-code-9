# -*- coding: utf-8 -*-
from suds import WebFault
from suds.client import Client


class DPDException(WebFault):
    """
    A generic exception type that can be handled by API consumers
    """
    pass


class DPDClient(object):
    """
    A DPD client API

    :param username: DPD Username (Also known as DelisId)
    :param password: DPD Password
    """

    # Caches for properties
    _login_service_client = None
    _shipment_service_client = None
    _depot_data_service_client = None
    _parcel_shop_finder_client = None
    _token = None

    def __init__(self, login_wsdl, shipment_service_wsdl,
                 depot_data_service_wsdl, parcel_shop_finder_service_wsdl,
                 username, password,
                 message_language='en_US'):
        self.login_wsdl = login_wsdl
        self.shipment_service_wsdl = shipment_service_wsdl
        self.depot_data_service_wsdl = depot_data_service_wsdl
        self.parcel_shop_finder_service_wsdl = parcel_shop_finder_service_wsdl

        self.username = username
        self.password = password

        self.message_language = message_language

    @property
    def login_service_client(self):
        """
        Returns a login service client
        """
        if self._login_service_client is None:
            self._login_service_client = Client(self.login_wsdl)
        return self._login_service_client

    @property
    def shipment_service_client(self):
        """
        Returns a shipment service client
        """
        if self._shipment_service_client is None:
            self._shipment_service_client = Client(self.shipment_service_wsdl)
        return self._shipment_service_client

    @property
    def depot_data_service_client(self):  # pragma: no cover
        """
        Returns a depot data service client
        """
        if self._depot_data_service_client is None:
            self._depot_data_service_client = Client(
                self.depot_data_service_wsdl
            )
        return self._depot_data_service_client

    @property
    def parcel_shop_finder_client(self):  # pragma: no cover
        """
        Returns a parcel shop finder client
        """
        if self._parcel_shop_finder_client is None:
            self._parcel_shop_finder_client = Client(
                self.parcel_shop_finder_service_wsdl
            )
        return self._parcel_shop_finder_client

    @property
    def token(self):
        """
        Returns the authentication token as a soap response
        """
        if self._token is None:
            self._token = self.get_auth()
        return self._token

    @property
    def soap_headers(self):
        """
        Returns the SOAP headers for requests which use token
        """
        return [{
            'delisId': self.token.delisId,
            'authToken': self.token.authToken,
            'messageLanguage': self.message_language,
        }]

    def get_auth(self):
        """
        Creates an authentication token for the committed user
        if user name and password are valid.

        The authentication token is needed for accessing other
        DPD Web Services.

        Returns an object with the ``auth_code`` attribute and ``depot``
        """
        try:
            response = self.login_service_client.service.getAuth(
                self.username, self.password, self.message_language
            )
        except WebFault, exc:
            raise DPDException(exc.fault, exc.document)
        else:
            return response

    def store_orders(self, print_options, shipment_service_data):
        """
        Call storeOrders service
        """
        self.shipment_service_client.set_options(soapheaders=self.soap_headers)
        try:
            response = self.shipment_service_client.service.storeOrders(
                print_options, shipment_service_data
            )
        except WebFault, exc:  # pragma: no cover
            raise DPDException(exc.fault, exc.document)
        else:
            return response

    def get_depot_data(self, country_code=None, depot=None, zip=None):
        """
        Call getDepotData service
        """
        self.depot_data_service_client.set_options(
            soapheaders=self.soap_headers
        )
        try:
            response = self.depot_data_service_client.service.getDepotData(
                country_code, depot, zip
            )
        except WebFault, exc:
            raise DPDException(exc.fault, exc.document)
        else:
            return response
