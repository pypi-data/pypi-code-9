from __future__ import unicode_literals

import six

from .. import Resource, SearchableResourceMeta


class Company(six.with_metaclass(SearchableResourceMeta, Resource)):
    path = 'company'
    search_path = 'search'
    attribute_names = [
        'duedil_url',
        # string the url of the full company profile on duedil.com
        'company_number',
        # string the company number
        'name',
        # string the company name
        'name_formated',
        # string a more readable version of the company name
        'registered_address',
        # obj Holds address information about the company
        'category',
        # string The category of company eg "Public Limited Company"
        'status',
        # string a string describing the status of company eg "In
        # Liquidation"
        'locale',
        # string Either "United Kingdom" or "Republic of Ireland"
        'previous_names',
        # array a collection containing one or more previous name
        # objects
        'sic_codes',
        # array a collection containing one or more SIC code objects
        'incorporation_date',
        # string when the company was incorporated. [YYYY-MM-DD]
        'accounts',
        # obj Information about the most recent accounts
        'returns',
        # obj information about the company's returns
    ]

    def __init__(self, api_key, company_number=None, **kwargs):
        super(Company, self).__init__(api_key=api_key, id=company_number, **kwargs)
