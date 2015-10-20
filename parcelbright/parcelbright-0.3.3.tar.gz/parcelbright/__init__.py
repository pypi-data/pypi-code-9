#!/usr/bin/env python
# encoding: utf-8

from dateutil.parser import parse as date_parse
import datetime
import logging
import json
import requests

from schematics import types
from schematics.exceptions import ConversionError
from schematics.types.compound import ModelType, ListType
from schematics.models import Model


__author__ = 'Marek Wywiał'
__email__ = 'onjinx@gmail.com'
__version__ = '0.3.3'


# configuration

#: `api_key` used to authorize with API
api_key = None

#: Whether use sandbox API version not
sandbox = False

#: Base url for production version
base_url = 'https://api.parcelbright.com/'

#: Base url for sandbox version
sandbox_base_url = 'https://api.sandbox.parcelbright.com/'


class DateTimeType(types.DateTimeType):

    def to_native(self, value, context=None):
        if isinstance(value, datetime.datetime):
            return value

        try:
            return date_parse(value)
        except (ValueError, TypeError):
            message = self.messages['parse'].format(value)
            raise ConversionError(message)


class ParcelBrightException(Exception):
    pass


class ValidationError(ParcelBrightException):
    """Raised when parcelbright entity like Address, Parcel or Shipment
    is invalid"""
    pass


class ShipmentNotCompletedException(ParcelBrightException):
    """Raised when `Shipment.state` is different than `completed`"""
    pass


class ParcelBrightAPIException(ParcelBrightException):
    """ParcelBright errors Base

    Args:
        message: error message
        response: requests.response instance
    """

    def __init__(self, message, response=None):
        super(Exception, self).__init__(message)
        self.response = response


class NotFound(ParcelBrightAPIException):
    """Raised when server response is 404"""
    pass


class BadRequest(ParcelBrightAPIException):
    """Raised when server response is 400"""
    pass


class TrackingError(BadRequest):
    """Raised when `Shipment.track()` responses with 400"""
    pass


class ParcelBrightError(object):
    """Handler for API errors"""

    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        try:
            self.debug = response.json()
        except (ValueError, TypeError):
            self.debug = {'message': response.content}

    def error_404(self):
        raise NotFound(
            '404 - {}'.format(self.debug.get('message')), self.response
        )

    def error_400(self):
        raise BadRequest('400 - {}, {}'.format(
            self.debug.get('message'),
            ['{}: {}'.format(e['field'], e['message'])
                for e in self.debug.get('errors', {})]
        ), self.response)

    def process(self):
        raise_error = getattr(self, 'error_{}'.format(self.status_code), False)
        if raise_error:
            raise raise_error()
        self.response.raise_for_status()


class Client(object):
    """Client to send configurated requests"""

    def __init__(self, api_key, sandbox=False, **kwargs):
        self.api_key = api_key
        self.sandbox = sandbox
        self.requester = requests.session()
        self.config = {
            'headers': {
                'Authorization': 'Token token="{}"'.format(self.api_key),
                'Accept': 'application/vnd.parcelbright.v1+json',
                'Content-Type': 'application/json',
            }
        }
        self.config.update(**kwargs)
        self.set_headers()
        if self.sandbox:
            self.config['base_url'] = sandbox_base_url
        else:
            self.config['base_url'] = sandbox_base_url

    @classmethod
    def instance(cls, **kwargs):
        return Client(api_key, sandbox, **kwargs)

    def set_headers(self):
        self.requester.headers.update(self.config.get('headers'))

    def request(self, verb, request, **kwargs):
        request = '{}{}'.format(
            self.config['base_url'], request
        )
        logging.debug(r'{}:{} -> {}'.format(
            verb, request, kwargs
        ))
        response = self.requester.request(verb, request, **kwargs)
        logging.debug(r'{}:{} <- {}'.format(
            verb, request, {
                'status_code': response.status_code,
            }
        ))
        ParcelBrightError(response).process()
        return response

    def get(self, request, **kwargs):
        response = self.request('get', request, **kwargs)
        # assert response.status_code == 200
        return response

    def post(self, request, **kwargs):
        response = self.request('post', request, **kwargs)
        # assert response.status_code == 201
        return response

    def patch(self, request, **kwargs):
        response = self.request('patch', request, **kwargs)
        # assert response.status_code == 200
        return response

    def put(self, request, **kwargs):
        response = self.request('put', request, **kwargs)
        # assert response.status_code == 200
        return response

    def delete(self, request, **kwargs):
        response = self.request('delete', request, **kwargs)
        # assert response.status_code == 204
        return response

    def head(self, request, **kwargs):
        return self.request('head', request, **kwargs)


class Parcel(Model):
    """Parcel container"""
    length = types.DecimalType(min_value=0, required=True)
    width = types.DecimalType(min_value=0, required=True)
    height = types.DecimalType(min_value=0, required=True)
    weight = types.DecimalType(min_value=0, required=True)

    def __repr__(self):
        return r'<Parcel [width={0.width}, height={0.height}, length={0.length}, weight={0.weight}]>'.format(self)  # NOQA


class Address(Model):

    """Address"""
    name = types.StringType(required=True, min_length=1)
    postcode = types.StringType(required=True, min_length=1)
    town = types.StringType(required=True, min_length=1)
    country_code = types.StringType(required=True, min_length=2, max_length=2)
    line1 = types.StringType(required=True, min_length=1)
    line2 = types.StringType(required=False)
    phone = types.StringType(required=True, regex='\d+')
    company = types.StringType(required=True, min_length=1)

    def __repr__(self):
        return r'<Address [name={0.name}, postcode={0.postcode}, town={0.town}, line1={0.line1}, country_code={0.country_code}]>'.format(self)  # NOQA


class ShipmentRate(Model):
    code = types.StringType(required=True)
    name = types.StringType(required=True)
    carrier = types.StringType(required=True)
    service_type = types.StringType(required=True)
    price = types.DecimalType(required=True)
    vat = types.DecimalType(required=True)
    pickup_date = types.DateType(required=True)
    transit_days = types.IntType(required=True)
    cutoff = DateTimeType(required=True)
    delivery_estimate = DateTimeType(required=True)


class ShipmentService(Model):
    code = types.StringType(required=True)
    name = types.StringType(required=True)
    price = types.DecimalType(required=True)
    carrier = types.StringType(required=True)
    service_type = types.StringType(required=True)
    vat = types.DecimalType(required=True)


class ShipmentTrack(Model):
    timestamp = types.DateType()
    location = types.StringType(required=False)
    description = types.StringType(required=False)
    detail = types.StringType(required=False)


class Shipment(Model):
    id = types.StringType(required=False)
    state = types.StringType(required=False, default='unknown')
    customer_reference = types.StringType(required=True)
    contents = types.StringType(required=True)
    estimated_value = types.DecimalType(min_value=0)
    pickup_date = types.DateType()
    parcel = ModelType(Parcel)
    to_address = ModelType(Address)
    from_address = ModelType(Address)
    liability_amount = types.DecimalType()
    pickup_confirmation = types.StringType()
    service = ModelType(ShipmentService)
    customs = types.StringType()
    customs_url = types.URLType()
    consignment = types.StringType()
    label_url = types.URLType()
    rates = ListType(ModelType(ShipmentRate))
    track = ListType(ModelType(ShipmentTrack))

    def __repr__(self):
        return r'<Shipment [id={0.id}, contents={0.contents}, state={0.state}]>'.format(self)  # NOQA

    def create(self):
        result = Client.instance().post(
            'shipments', data=json.dumps({'shipment': self.to_primitive()})
        ).json()['shipment']
        return self.import_data(result)

    @classmethod
    def find(cls, id):
        return Shipment.from_flat(Client.instance().get(
            'shipments/{}'.format(id),
        ).json()['shipment'])

    def book(self, rate_code, pickup_date=None):
        data = {
            'rate_code': rate_code,
        }
        if pickup_date:
            data['pickup_date'] = pickup_date

        Client.instance().post(
            'shipments/{}/book'.format(self.id),
            data=json.dumps(data)
        )
        self.import_data(
            Shipment.find(self.id).flatten()
        )

    def track(self, refresh=False):
        if not self.state == 'completed':
            raise ShipmentNotCompletedException('''
            Missing `shipment.consignment` value. You have to run
            `shipment.book()` first''')

        if 'events' not in self.__dict__ or refresh:
            try:
                self.__dict__.update(
                    Client.instance().get(
                        'shipments/{}/track'.format(self.id)
                    ).json()
                )
            except BadRequest as e:
                raise TrackingError(e.message, e.response)

        return self.events

    def cancel(self):
        Client.instance().post(
            'shipments/{}/cancel'.format(self.id)
        )
        self.__dict__.update(
            Shipment.find(self.id).__dict__
        )
