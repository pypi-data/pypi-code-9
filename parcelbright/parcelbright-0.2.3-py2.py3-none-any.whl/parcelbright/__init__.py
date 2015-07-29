#!/usr/bin/env python
# encoding: utf-8

import json
import requests


__author__ = 'Marek Wywiał'
__email__ = 'onjinx@gmail.com'
__version__ = '0.2.3'


# configuration

#: `api_key` used to authorize with API
api_key = None

#: Whether use sandbox API version not
sandbox = False

#: Base url for production version
base_url = 'https://api.parcelbright.com/'

#: Base url for sandbox version
sandbox_base_url = 'https://api.sandbox.parcelbright.com/'


class ParcelBrightException(Exception):
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
        response = self.requester.request(verb, request, **kwargs)
        ParcelBrightError(response).process()
        return response

    def get(self, request, **kwargs):
        response = self.request('get', request, **kwargs)
        assert response.status_code == 200
        return response

    def post(self, request, **kwargs):
        response = self.request('post', request, **kwargs)
        assert response.status_code == 201
        return response

    def patch(self, request, **kwargs):
        response = self.request('patch', request, **kwargs)
        assert response.status_code == 200
        return response

    def put(self, request, **kwargs):
        response = self.request('put', request, **kwargs)
        assert response.status_code == 200
        return response

    def delete(self, request, **kwargs):
        response = self.request('delete', request, **kwargs)
        assert response.status_code == 204
        return response

    def head(self, request, **kwargs):
        return self.request('head', request, **kwargs)


def todict(obj):
    """Transforms `Entity` or embedded in dictionary `Entities` into plain
    dictionary

    Args:
        obj: `Entity` or dictionary
    Returns:
        A plain dictionary of public attributes from `Entity`
    """

    try:
        return obj.dict()
    except AttributeError:
        result = {}
        for k, v in obj.items():
            try:
                result[k] = v.dict()
            except AttributeError:
                result[k] = v
        return result


class Entity(object):
    def dict(self):
        """Returns `Entity` dictionary for existing, public, not `None`
        attributes"""

        result = {}
        for k, v in self.__dict__.items():
            if v is None or k.startswith('_'):
                continue
            result[k] = v
        return result


class Parcel(Entity):
    """Parcel container"""

    def __init__(self, length, width, height, weight):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def __repr__(self):
        return r'<Parcel [width={0.width}, height={0.height}, length={0.length}, weight={0.weight}]>'.format(self)  # NOQA


class Address(Entity):

    """Address"""

    def __init__(
            self, name, postcode, town, line1, phone, country_code, line2=None,
            company=None
    ):
        self.name = name
        self.postcode = postcode
        self.town = town
        self.country_code = country_code
        self.line1 = line1
        self.line2 = line2
        self.phone = phone
        self.company = company

    def __repr__(self):
        return r'<Address [name={0.name}, postcode={0.postcode}, town={0.town}, line1={0.line1}, country_code={0.country_code}]>'.format(self)  # NOQA


class Shipment(Entity):
    def __init__(
        self, customer_reference, contents, estimated_value, parcel,
        to_address, from_address, customs_form=None, pickup_date=None,
        liability_amount=None, **kwargs
    ):
        # defaults
        self.id = None
        self.state = 'unknown'

        # passed
        self.customer_reference = customer_reference
        self.contents = contents
        self.estimated_value = estimated_value
        self.parcel = parcel
        self.to_address = to_address
        self.from_address = from_address
        self.customs_form = customs_form
        self.pickup_date = pickup_date
        self.liability_amount = liability_amount
        self.__dict__.update(kwargs)

    def __repr__(self):
        return r'<Shipment [id={0.id}, contents={0.contents}, state={0.state}]>'.format(self)  # NOQA

    @classmethod
    def create(cls, **kwargs):
        return cls(**Client.instance().post(
            'shipments', data=json.dumps({'shipment': todict(kwargs)})
        ).json()['shipment'])

    @classmethod
    def find(cls, id):
        return cls(**Client.instance().get(
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
        self.__dict__.update(
            Shipment.find(self.id).__dict__
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
