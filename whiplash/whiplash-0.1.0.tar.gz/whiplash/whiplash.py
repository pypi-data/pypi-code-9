# -*- coding: utf-8 -*-
"""
whiplash.py
"""
import requests
import json


class Whiplash(object):
    "API Client for talking to Whiplash"

    test_url = 'https://testing.whiplashmerch.com'
    production_url = 'https://www.whiplashmerch.com'

    def __init__(self, api_key, test=False):
        self.api_key = api_key
        self.test = test
        self.item = ItemClient(self)
        self.order = OrderClient(self)
        self.order_item = OrderItemClient(self)
        self.ship_notice = ShipNoticeClient(self)
        self.ship_notice_item = ShipNoticeItemClient(self)

        self.session = requests.Session()
        self.session.headers.update({
            'X-API-VERSION': '1',
            'X-API-KEY': self.api_key,
            'content-type': 'application/json',
        })

    @property
    def url(self):
        if self.test:
            return self.test_url
        return self.production_url


class WhiplashException(Exception):
    pass


class BaseClient(object):

    def __init__(self, client):
        self.client = client

    def process(self, response):
        print response.status_code, response.content
        response.raise_for_status()
        return response.json()

    def _get(self, path, params=None):
        return self.process(
            self.client.session.get(
                self.client.url + self.base_path + path,
                params=params
            )
        )

    def _post(self, path, payload=None):
        return self.process(
            self.client.session.post(
                self.client.url + self.base_path + path,
                data=json.dumps(payload)
            )
        )

    def _put(self, path, params=None):
        return self.process(
            self.client.session.put(
                self.client.url + self.base_path + path,
                params=params
            )
        )

    def _delete(self, path=None, params=None):
        return self.process(
            self.client.session.delete(
                self.client.url + self.base_path + path,
                params=params
            )
        )


class Resource(object):

    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        if hasattr(self.client, name):
            return getattr(self.client, name)
        raise AttributeError(name)


class Order(Resource):
    pass


class OrderClient(BaseClient):

    base_path = '/api/orders'

    def list(self, **kwargs):
        return self._get('', kwargs)

    def count(self, **kwargs):
        return self._get('/count', kwargs)

    def get(self, order_id=None, originator_id=None):
        if not (order_id or originator_id):
            raise WhiplashException('Must specify order id or originator id')

        if order_id:
            return Order(self._get('/%s' % order_id))
        else:
            return Order(self._get('/originator/%s' % originator_id))

    def create(self, **kwargs):
        return Order(self._post('', kwargs))

    def update(self, order_id, **kwargs):
        return self._put('/%s' % order_id, kwargs)

    def cancel(self, order_id):
        return self._put('/%s/cancel' % order_id)

    def uncancel(self, order_id):
        return self._put('/%s/uncancel' % order_id)

    def pause(self, order_id):
        return self._put('/%s/pause' % order_id)

    def release(self, order_id):
        return self._put('/%s/release' % order_id)

    def packages(self, order_id):
        return self._get('/%s/packages' % order_id)


class OrderItem(Resource):
    pass


class OrderItemClient(BaseClient):

    base_path = '/api/order_items'

    def list(self, order_id):
        return self._get('', {'order_id': order_id})

    def get(self, order_item_id=None, originator_id=None):
        if not (order_item_id or originator_id):
            raise WhiplashException(
                'Must specify order item id or originator id'
            )
        if order_item_id:
            return OrderItem(
                self.client,
                self._get('/%s' % order_item_id),
            )
        else:
            return OrderItem(
                self.client,
                self._get('/originator/%s' % originator_id),
            )

    def create(self, **kwargs):
        return OrderItem(
            self.client,
            self._post('', kwargs),
        )

    def update(self, order_item_id, **kwargs):
        return self._put('/%s' % order_item_id, kwargs)

    def delete(self, order_item_id):
        return self._delete('/%s' % order_item_id)


class Item(Resource):
    pass


class ItemClient(BaseClient):

    base_path = '/api/items'

    def list(self, **kwargs):
        return self._get('', kwargs)

    def count(self, **kwargs):
        return self._get('/count', kwargs)

    def create(self, **kwargs):
        return Item(self.client, self._post('', kwargs))

    def update(self, item_id, **kwargs):
        return self._put('/%s' % item_id, kwargs)

    def deactivate(self, item_id):
        return self._delete('/%s' % item_id)

    def transactions(self, item_id, **kwargs):
        return self._get('/%s/transactions' % item_id, kwargs)

    def warehouse_quantities(self, item_id):
        return self._get('/%s/warehouse_quantities' % item_id)

    def get(self, item_id=None, originator_id=None, sku=None, group_id=None):
        if not (item_id or originator_id):
            raise WhiplashException(
                'Must specify item id or originator id'
            )
        if item_id:
            return Item(
                self.client,
                self._get('/%s' % item_id),
            )
        else:
            return Item(
                self.client,
                self._get('/originator/%s' % originator_id),
            )

    def get_by(self, sku=None, group_id=None):
        if not (sku or group_id):
            raise WhiplashException(
                'Must specify SKU or Group Id'
            )
        if sku:
            return [
                Item(self.client, item)
                for item in self._get('/sku/%s' % sku)
            ]
        else:
            return [
                Item(self.client, item)
                for item in self._get('/group/%s' % group_id)
            ]

    def inbound(self):
        return [
            Item(self.client, item)
            for item in self._get('/inbound')
        ]

    def in_bundles(self):
        return [
            Item(self.client, item)
            for item in self._get('/in_bundles')
        ]

    def bundles(self):
        return [
            Item(self.client, item)
            for item in self._get('/bundle_items')
        ]


class ShipNoticeClient(BaseClient):

    base_path = '/api/shipnotices'

    def list(self, **kwargs):
        return self._get('', kwargs)

    def count(self, **kwargs):
        return self._get('/count', kwargs)

    def get(self, shipnotice_id):
        return self._get('/%s' % shipnotice_id)

    def create(self, **kwargs):
        return self._post('', kwargs)

    def update(self, shipnotice_id, **kwargs):
        return self._put('/%s' % shipnotice_id, kwargs)

    def delete(self, shipnotice_id):
        return self._delete('/%s' % shipnotice_id)


class ShipNoticeItemClient(BaseClient):

    base_path = '/api/shipnotice_items'

    def list(self, shipnotice_id, **kwargs):
        kwargs['shipnotice_id'] = shipnotice_id
        return self._get('', kwargs)

    def get(self, shipnotice_item_id):
        return self._get('/%s' % shipnotice_item_id)

    def create(self, **kwargs):
        return self._post('', kwargs)

    def update(self, shipnotice_item_id, **kwargs):
        return self._put('/%s' % shipnotice_item_id, kwargs)

    def delete(self, shipnotice_item_id):
        return self._delete('/%s' % shipnotice_item_id)
