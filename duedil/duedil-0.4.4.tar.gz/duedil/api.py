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


from .search.lite import CompanySearchResult as LiteCompanySearchResult
from .search.pro import CompanySearchResult as ProCompanySearchResult, DirectorSearchResult
from .search.international import CompanySearchResult as InternationalCompanySearchResult

import os
import json

import requests
from requests.exceptions import HTTPError

try:  # pragma: no cover
    long
except NameError:  # pragma: no cover
    # Python 3
    long = int

try:  # pragma: no cover
    unicode
except NameError:  # pragma: no cover
    # Python 3
    basestring = unicode = str

API_URLS = {
    'pro': 'http://duedil.io/v3',
    'lite': 'http://api.duedil.com/open',
    'international': 'http://api.duedil.com/international',
}
API_KEY = os.environ.get('DUEDIL_API_KEY', None)


class Client(object):
    cache = None
    base_url = None

    def __init__(self, api_key=None, sandbox=False, cache=None):
        'Initialise the Client with which API to connect to and what cache to use'
        self.cache = cache
        self.set_api(api_key, sandbox)

    def set_api(self, api_key=None, sandbox=False):

        if not (api_key or API_KEY):
            raise ValueError("Please provide a valid Duedil API key")
        self.api_key = api_key or API_KEY

        try:
            self.base_url = API_URLS.get(self.api_type, 'lite')
        except AttributeError:
            raise ValueError('Duedil API type must be "{}"'.format('", "'.join(API_URLS.keys())))

        # Are we in a sandbox?
        self.sandbox = sandbox
        if self.sandbox:
            self.base_url = self.base_url + '/sandbox'

    def get(self, endpoint, data=None):
        return self._get(endpoint, data)

    def _get(self, endpoint, data=None):
        'this should become the private interface to all reequests to the api'

        result = None
        data = data or {}

        if self.api_type in ["pro", "lite"]:
            data_format = 'json'
            resp_format = '.{}'.format(data_format)
        else:
            resp_format = ''



        url = "{base_url}/{endpoint}{format}"
        prepared_url = url.format(base_url=self.base_url,
                                  endpoint=endpoint,
                                  format=resp_format)

        if self.cache:
            result = self.cache.get_url(prepared_url, url_params=data)

        if not result:
            params = data.copy()
            params['api_key'] = self.api_key
            response = requests.get(prepared_url, params=params)
            try:
                if not response.raise_for_status():
                    result = response.json()
                    if self.cache:
                        self.cache.set_url(prepared_url, result,
                                           url_params=params)
            except HTTPError:
                if response.status_code == 404:
                    result = {}
                else:
                    raise
        return result

    def _search(self, endpoint, result_klass, *args, **kwargs):
        query_params = self._build_search_string(*args, **kwargs)
        results = self._get(endpoint, data=query_params)
        return [result_klass(self, **r) for r in results.get('response',{}).get('data', {})]

    def _build_search_string(self, *args, **kwargs):
        data = {}
        try:
            data['q'] = kwargs['query']
        except KeyError:
            raise ValueError('query key must be present as a kwarg')
        return data

    def search(self, query):
        raise NotImplementedError


class LiteClient(Client):
    api_type = 'lite'

    def search(self, query):
        #  this will need to be alter in all likely hood to do some validation
        return self._search('search', LiteCompanySearchResult, query=query)


class ProClient(Client):
    api_type = 'pro'
    company_term_filters = [
        "locale",
        "location",
        "postcode",
        "sic_code",
        "sic_2007_code",
        "status",
        "currency",
        "keywords",
        "name",
    ]
    company_range_filters = [
        "employee_count",
        "turnover",
        "turnover_delta_percentage",
        "gross_profit",
        "gross_profit_delta_percentage",
        "cost_of_sales",
        "cost_of_sales_delta_percentage",
        "net_assets",
        "net_assets_delta_percentage",
        "current_assets",
        "current_assets_delta_percentage",
        "total_assets",
        "total_assets_delta_percentage",
        "cash",
        "cash_delta_percentage",
        "total_liabilities",
        "total_liabilities_delta_percentage",
        "net_worth",
        "net_worth_delta_percentage",
        "depreciation",
        "depreciation_delta_percentage",
        "taxation",
        "retained_profits",
        "profit_ratio",
        "inventory_turnover_ratio",
        "net_profitability",
        "return_on_capital_employed",
        "cash_to_total_assets_ratio",
        "gearing",
        "gross_margin_ratio",
        "return_on_assets_ratio",
        "current_ratio",
        "debt_to_capital_ratio",
        "cash_to_current_liabilities_ratio",
        "liquidity_ratio",
    ]
    director_term_filters = [
        "name",
        "gender",
        "title",
        "nationality",
        "secretarial",
        "corporate",
        "disqualified",
    ]
    director_range_filters = [
        "age",
        "data_of_birth",
        "gross_profit",
        "gross_profit_delta_percentage",
        "turnover",
        "turnover_delta_percentage",
        "cost_of_sales",
        "cost_of_sales_delta_percentage",
        "depreciation",
        "depreciation_delta_percentage",
        "taxation",
        "cash",
        "cash_delta_percentage",
        "net_worth",
        "net_worth_delta_percentage",
        "total_assets",
        "total_assets_delta_percentage",
        "current_assets",
        "current_assets_delta_percentage",
        "net_assets",
        "net_assets_delta_percentage",
        "total_liabilities",
        "total_liabilities_delta_percentage",
    ]

    def _build_search_string(self, term_filters, range_filters,
                             order_by=None, limit=None, offset=None,
                             **kwargs):
        data = {}
        for arg, value in kwargs.items():
            if arg in term_filters:
                # this must be  a string
                try:
                    assert(isinstance(value, basestring))
                except AssertionError:
                    raise TypeError('%s must be string type' % arg)
            elif arg in range_filters:
                # array of two numbers
                try:
                    assert(isinstance(value, (list, tuple)))
                except AssertionError:
                    raise TypeError('%s must be an array' % arg)
                try:
                    assert(len(value) == 2)
                except AssertionError:
                    raise ValueError('Argument %s can only be an array of length 2' % arg)
                for v in value:
                    try:
                        assert(isinstance(v, (int, long, float)))
                    except AssertionError:
                        raise TypeError('Value of %s must be numeric' % arg)
            else:
                raise TypeError('%s does not match %s' % (arg, ', '.join(term_filters+range_filters)))
        data['filters'] = json.dumps(kwargs)
        if order_by:
            try:
                assert(isinstance(order_by, dict))
            except:
                raise TypeError('order_by must be dictionary')
            try:
                assert('field' in order_by)
            except AssertionError:
                raise ValueError("'field' must be a key in the order_by dictionary")
            try:
                assert(order_by['field'] in term_filters + range_filters)
            except AssertionError:
                raise TypeError("order_by['field'] must be one of %s" % (', '.join(term_filters+range_filters)))
            if order_by.get('direction'):
                try:
                    assert(order_by['direction'] in ['asc', 'desc'])
                except AssertionError:
                    raise ValueError('The direction must either be "asc" or "desc"')
            data['orderBy'] = json.dumps(order_by)
        if limit:
            try:
                assert(isinstance(limit, int))
            except AssertionError:
                raise TypeError('limit must be an integer')
            data['limit'] = limit
        if offset:
            try:
                assert(isinstance(offset, int))
            except AssertionError:
                raise TypeError('offset must be an integer')
            data['offset'] = offset
        return data

    def search_company(self, order_by=None, limit=None, offset=None, **kwargs):
        '''
        Conduct advanced searches across all companies registered in
        UK & Ireland.
        Apply any combination of 44 different filters

        The parameter filters supports two different types of queries:
            * the "range" type (ie, a numeric range) and
            * the "terms" type (for example, an individual company name).

        For the range filter, you have to pass an array;
        for the terms filter, you just pass a string.

        The range type is used when you want to limit the results to a
        particular range of results.

        You can order the results based on the ranges using the
        parameter orderBy.
        '''
        return self._search('companies',
                            ProCompanySearchResult,
                            self.company_term_filters,
                            self.company_range_filters,
                            order_by=order_by,
                            limit=limit,
                            offset=offset,
                            **kwargs)

    def search_director(self, order_by=None, limit=None, offset=None, **kwargs):
        '''
        This "Director search endpoint" is similar to the
        "Company search endpoint", though with some different ranges and
        terms.

        Searching by financial range will return directors who have a
        directorship at a company fulfilling that range.

        NB: The location filter is not available for director search.
        '''
        return self._search('directors',
                            DirectorSearchResult,
                            self.director_term_filters,
                            self.director_range_filters,
                            order_by=order_by,
                            limit=limit,
                            offset=offset,
                            **kwargs)

    def search(self, order_by=None, limit=None, offset=None, **kwargs):
        return self.search_company(order_by, limit, offset, **kwargs) + \
               self.search_director(order_by, limit, offset, **kwargs)


class InternationalClient(Client):
    api_type = 'international'

    def search(self, country_code, query):
        endpoint = '{}/search'.format(country_code)
        return self._search(endpoint, InternationalCompanySearchResult, query=query)

    def get(self, country_code, endpoint, data):
        endpoint = '{}/{}'.format(country_code, endpoint)
        return self._get(endpoint, data)

    # this should be a Resource and not here...
    def report(self, country_code, id):
        return self.get(country_code, 'report/{}'.format(id), {})
