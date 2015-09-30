# -*- coding: utf-8 -*-
#
#  DuedilApiClient v3 Pro
#  @copyright 2014 Christian Ledermann
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

from __future__ import unicode_literals

import sys
import six
import json

from ..api import LiteClient, ProClient#, InternationalClient


class Resource(object):
    attribute_names = None
    locale = 'uk'
    id = None
    path = None
    client_class = LiteClient

    def __init__(self, id, api_key=None, locale='uk', load=False, **kwargs):
        if not self.attribute_names:
            raise NotImplementedError(
                "Resources must include a list of allowed attributes")

        self.id = id
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        self.client = self.client_class(api_key, sandbox=kwargs.pop('sandbox', False))

        if load:
            self.load()

        if kwargs:
            self._set_attributes(**kwargs)

    def _set_attributes(self, missing=False, **kwargs):
        for k, v in kwargs.items():
            if k in self.attribute_names:
                self.__setattr__(k, v)

        if missing is True:
            for allowed in self.attribute_names:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)

    def load(self):
        result = self.client.get(self.endpoint)
        self._set_attributes(**result)

    def __getattr__(self, name):
        """
        lazily return attributes, only contact duedil if necessary
        """
        try:
            return super(Resource, self).__getattribute__(name)
        except AttributeError:
            if name in self.attribute_names:
                self.load()
                return super(Resource, self).__getattribute__(name)
            else:
                raise

    @property
    def endpoint(self):
        if not self.path:
            raise ValueError(
                "{model} does not have a path to load specified".format(
                    model=self.__class__.__name__))
        endpoint = '{locale}/{path}'.format(locale=self.locale,
                                            path=self.path)
        if self.id:
            endpoint += '/{id}'.format(id=self.id)
        return endpoint


class ProResource(Resource):
    client_class = ProClient

    def _assign_attributes(self, data=None):
        # assert(data['response'].get('id') == self.id), \
            # 'Requested company ID does not match specified ID, something gone wrong!'
        self._set_attributes(missing=True, **data['response'])

    def load(self):
        """
        get results from duedil
        """
        result = self.client.get(self.endpoint)
        self._assign_attributes(result)






# Here be metaclass dragons that don't make complete sense as to why we have them


def resource_property(endpoint):
    def wrap(getter_fn):
        def inner(self, *args, **kwargs):
            return getter_fn(self, endpoint, *args, **kwargs)
        return inner
    return wrap


class SearchableResourceMeta(type):
    term_filters = None
    range_filters = None
    search_path = None

    def search(klass, order_by=None, limit=None, offset=None, **kwargs):
        data = klass.client._build_search_string(klass.term_filters,
                                                 klass.range_filters,
                                                 order_by=order_by, limit=limit,
                                                 offset=offset, **kwargs)
        results_raw = klass.client.get(klass.search_path, data=data)
        results = []
        for r in results_raw['response']['data']:
            results.append(
                klass(**r)
            )
        return results

from importlib import import_module

class RelatedResourceMeta(type):

    def __init__(klass, name, bases, ns):
        related_resources = ns.get('related_resources') or {}

        for ep in related_resources.keys():

            @resource_property(ep)
            def getter(self, endpoint):
                resource = self.related_resources[endpoint]

                if isinstance(resource, six.string_types):
                    module, resource = resource.rsplit('.', 1)
                    resource = getattr(sys.modules['duedil.%s' % module], resource)

                return self.load_related(endpoint, resource)

            attr_name = ep.replace('-', '_')
            setattr(klass, attr_name,
                    property(getter, None, None, attr_name))

class SearchableRelatedResourceMeta(SearchableResourceMeta, RelatedResourceMeta):
    pass


class RelatedResourceMixin(six.with_metaclass(RelatedResourceMeta, object)):
    related_resources = None

    def _get(self, resource):
        uri = '{endpoint}/{resource}'.format(endpoint=self.endpoint,
                                             resource=resource)
        return self.client.get(uri)

    def load_related(self, key, klass=None):
        internal_key = '_' + key.replace('-', '_')


        related = getattr(self, internal_key, None)

        if related is None:
            result = self._get(key)
            if result:
                response = result['response']
                related = None
                if (
                    'data' in response and
                    isinstance(response['data'], (list, tuple))
                ):
                    related = []
                    for r in result['response']['data']:
                        r['locale'] = r.get('locale', self.locale)
                        related.append(
                            klass(api_key=self.client.api_key, **r) if klass else None
                        )
                elif result:
                    response['locale'] = response.get('locale', self.locale)
                    if klass:
                        print(response)
                        related = klass(api_key=self.client.api_key, **response)
                setattr(self, internal_key, related)
        return related
