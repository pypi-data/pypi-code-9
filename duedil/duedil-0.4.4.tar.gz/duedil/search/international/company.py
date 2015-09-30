
from .. import SearchResource


class CompanySearchResult(SearchResource):
    attribute_names = [
        'registration_number'
        'name'
        'type'
        'status'
        'address'
        'office_type'
        'country'
        'date_of_latest_accounts'
        'online_reports'
        'available_report_types'
        'available_languages'
    ]
