# -*- coding: utf-8 -*-
import json
import logging
from functools import partial

import requests


class FlipkartAPI(object):
    """
    Flipkart Marketplace Seller API Client.

    This client provides access to flipkart objects (orders, skus) in a generic
    way.

    You can read more about `Flipkart Marketplace API here
    <https://seller.flipkart.com/api-docs/FMSAPI.html>`_

    :param access_token: Access token received at the end of an Authorization
                         Code Flow or Client Credentials Flow.
    :param sandbox: True/False to connect to sandbox or not (Default: connects
                    to production)
    :param debug: If enabled, spits out debug logs.

    Example::

        from flipkart import FlipkartAPI
        flipkart = FlipkartAPI(access_token='your_access_token')

    """
    def __init__(self, access_token, sandbox=False, debug=False):
        self.access_token = access_token
        self.sandbox = sandbox
        self.debug = debug

        self.session = self.get_session()
        self.logger = self.get_logger()

    def get_session(self):
        """
        Build a requests session that can be used to hold
        the authorization
        """
        session = requests.Session()
        session.headers.update({
            'Authorization': 'Bearer %s' % self.access_token,
            'Content-type': 'application/json',
        })
        return session

    def get_logger(self):
        """
        Return a logger
        """
        logger = logging.getLogger('flipkart')
        logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if self.debug else logging.INFO)
        logger.addHandler(ch)

        return logger

    def build_url(self, path, params=None):
        """
        Given a path construct the full URL for sandbox or production
        """
        # TODO: Handle parameters
        if path.startswith('/'):
            path = path[1:]

        if self.sandbox:
            return 'https://sandbox-api.flipkart.net/sellers/' + path
        else:
            return 'https://api.flipkart.net/sellers/' + path

    def request(self, path, params=None, body=None, method="GET"):
        """
        Makes a request and sends the response body back.
        """
        url = self.build_url(path, params)
        self.logger.debug("Request:URL: %s", url)
        self.logger.debug("Request:Method: %s", method)

        if body is not None:
            payload = json.dumps(body)
        else:
            payload = None

        self.logger.debug("Request:Payload: %s", payload)

        if method == 'GET':
            response = self.session.get(url, data=payload, verify=False)
        elif method == 'POST':
            response = self.session.post(url, data=payload, verify=False)
        else:
            raise ValueError('Unknown method %s' % method)

        self.logger.debug("Response:code: %s", response.status_code)
        self.logger.debug("Response:content: %s", response.content)

        # Raise an error if the response is not 2XX
        response.raise_for_status()

        response_json = response.json()

        if response_json.get('status') == 'failure':
            raise FlipkartMultiError(response_json['errors'])

        return response_json

    def sku(self, sku_id):
        """
        Get a SKU
        """
        return SKU(sku_id, self)

    def listing(self, listing_id):
        """
        Get a listing
        """
        return Listing(listing_id, sku=None, client=self, lazy=False)

    def bulk_listing(self, listings):
        """
        Create and update listing attributes such as stock, price, and
        procurement SLA for multiple SKUs. A maximum of 10 listings can be
        updated.
        """
        raise Exception('Not implemented yet')

    def search_orders(self, filters=None, page_size=None, sort=None):
        """
        Search through the orders
        """
        return OrderItem.search(self, filters, page_size, sort)


class BaseFlipkartError(Exception):
    """
    Base class for all flipkart exceptions
    """
    pass


class FlipkartError(BaseFlipkartError):
    """
    Base class for Flipkart exceptions
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(FlipkartError, self).__init__(code, message)


class FlipkartMultiError(BaseFlipkartError):
    """
    An API request could result in multiple errors. This abstracts away the
    detail by showing multiple errors
    """
    def __init__(self, errors):
        self.errors = []
        for error in errors:
            self.errors.append(
                FlipkartError(error['errorCode'], error['message'])
            )
        super(FlipkartMultiError, self).__init__(
            '%d errors in request' % len(self.errors)
        )


class FlipkartCollection(object):
    """
    Common parent class for collections like orders
    """
    pass


class FlipkartResource(object):
    """
    Common parent class for flikart resources like SKUs, listing etc
    """
    pass


class SKU(FlipkartResource):
    """
    Represents a SKU ientified by a SKU ID.

    :param sku_id: ID of the SKU
    :param client: The client connection the SKU will use to fetch and update
    """
    def __init__(self, sku_id, client):
        self.sku_id = sku_id
        self.client = client

    def create_listing(self, **attributes):
        """
        Creates a listing for the SKU with the given attributes. The listing
        is not saved and must be explicitly saved by the user.

        Example::

            new_listing = sku.create_listing(
                mrp=100
            )
            new_listing.save()
        """
        return Listing(
            listing_id=None, client=self.client,
            sku=self, attributes=attributes
        )

    @property
    def listings(self):
        """
        Return a list of listings, but it seems like flipkart allows only
        one listing per seller. So this should usually return just one listing.
        However, to keep the API consistent, this will return a list
        """
        response = self.client.request(
            'skus/%s/listings' % self.sku_id,
        )
        return [
            Listing(
                response['listingId'],
                self, self.client,
                attributes=response['attributeValues']
            )
        ]


class OrderItem(FlipkartResource):
    """
    Represents an order item with ID order_item_id.
    An order represented by OrderId could have items from multiple sellers
    and the seller only has access to order_item_id(s).
    """

    def __init__(self, order_item_id, client, attributes=None):
        self.order_item_id = order_item_id
        self.attributes = attributes

    def refresh_attributes(self):
        """
        Fetch the order attributes from flipkart
        """
        response = self.client.request(
            'orders/%s' % self.order_item_id
        )
        self.attributes = response

    def __getattr__(self, name):
        if self.attributes is not None and name in self.attributes:
            return self.attributes[name]
        raise AttributeError(name)

    @classmethod
    def search(cls, client, filters=None, page_size=None, sort=None):
        """
        Search for orders that meet the criteria.

        :param sort: A tuple of field and sort order Ex: `('orderDate', 'asc')`
        """
        body = {
            'filter': filters or {},
        }

        if page_size is not None:
            body['pagination'] = {
                'pageSize': page_size
            }

        if sort is not None:
            body['sort'] = {
                'field': sort[0],
                'order': sort[1],
            }

        response = client.request(
            'orders/search',
            body=body,
            method="POST"
        )
        return PaginationIterator(
            client, response,
            'orderItems',
            lambda item: partial(cls, client=client)(
                item['orderItemId'], attributes=item
            )
        )


class PaginationIterator(object):
    """
    An iterable that lets the user infinitely browse through pages of a
    paginated response

    :param client: The API client to make subsequent requests with
    :param response: The dictionary of response with pagination
    :param key: The key that identifies the item iterable (ex:orderItems)
    :param cast_func: Each item in iterable is casted with this function
                      if specidied
    """
    def __init__(self, client, response, key, cast_func=None):
        self.client = client
        self.items = []
        self.key = key

        if cast_func is None:
            cast_func = lambda item: item
        self.cast_func = cast_func

        self._nextPageUrl = None

        self.update_items_from(response)

    def update_items_from(self, response):
        """
        Given a response dictionary, update the items and urls
        """
        self.items.extend(response[self.key])
        self._nextPageUrl = response.get('nextPageUrl')

    def __iter__(self):
        self._current_index = -1
        return self

    @property
    def count(self):
        return len(self.items)

    def __next__(self):
        self._current_index += 1

        if self._current_index >= self.count and self._nextPageUrl:
            # If the iterator has reached its end and there is a
            # nextPageUrl then get the fresh items and update
            self.update_items_from(self.client.request(self._nextPageUrl))

        if self._current_index < self.count:
            return self.cast_func(self.items[self._current_index])
        else:
            raise StopIteration()

    next = __next__


class Listing(FlipkartResource):
    """
    Represents a Listing for a SKU
    """
    def __init__(self, listing_id, sku, client, attributes=None, lazy=True):
        self.listing_id = listing_id
        self.sku = sku
        self.client = client
        self.attributes = attributes

        if self.listing_id and not self.attributes and not lazy:
            self.refresh_attributes()

    @classmethod
    def new(cls, client, sku, attributes):
        """
        Create a new listing with the given attributes. This is not meant to
        be called directly, but through `sku.create_listing(mrp=100)` style.
        """
        return cls(listing_id=None, sku=sku, attributes=attributes)

    def refresh_attributes(self):
        """
        Fetch the attributes from flipkart
        """
        if self.listing_id is None:
            raise ValueError('Cannot fetch attributes for an unsaved listing')

        response = self.client.request(
            'skus/listings/%s' % self.listing_id
        )

        if self.sku is None:
            # Set the sku if the SKU was not known before
            self.sku = SKU(response['skuId'], self.client)

        self.attributes = response['attributeValues']
        return response

    def update(self, attributes):
        """
        Update listing attributes such as stock, price, and pocurement SLA
        for a particular ListingID. For a more convenient API use
        `listing.save()` once the attributes have been changed.
        """
        self.attributes = self.client.request(
            'skus/listings/%s' % self.listing_id,
            body={'attributeValues': attributes},
            method="POST"
        )['response']['attributeValues']
        return self.attributes

    def save(self):
        """
        Save any changes to the listing by updating it
        """
        if self.listing_id:
            return self.update(self.attributes)
        else:
            # This is a new listing. So create a new listing
            response = self.client.request(
                "skus/%s/listings" % self.sku.sku_id,
                body={
                    'fsn': None,    # XXX: Where is that coming from ??
                    'attributeValues': self.attributes,
                },
                method="POST"
            )['response']
            self.listing_id = response['listingId']
            self.refresh_attributes()
