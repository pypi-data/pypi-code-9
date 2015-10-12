

# from ...resources import Resource
from .. import SearchResource


class CompanySearchResult(SearchResource):
    attribute_names = [
        'locale'
        'name'
        'name_formatted'
        'link'
    ]

    def __init__(self, client, company_number=None, **kwargs):
        super(CompanySearchResult, self).__init__(client, rid=company_number, **kwargs)
