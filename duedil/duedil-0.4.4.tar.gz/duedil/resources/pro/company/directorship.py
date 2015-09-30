from __future__ import unicode_literals

from ... import ProResource


class Directorship(ProResource):
    attribute_names = [
        'id',
        # string Director ID
        'last_update',
        # dateTime Date last updated
        'active',
        # boolean Active (true/false)
        'status',
        # string Status
        'founding',
        # boolean Founding director (true/false)
        'appointment_date',
        # dateTime Date appointed
        'function',
        # string Function
        'function_code',
        # integer Function code
        'position',
        # string Position
        'position_code',
        # string Position code
        'companies_url',
        # string Link to companies
        'directors_uri',
        # string Link to director profile
        'service_address_uri',
        # string Link to service address
        'address1',
        # string Address line 1
        'address2',
        # string Address line 2
        'address3',
        # string Address line 3
        'address4',
        # string Address line 4
        'address5',
        # string Address line 5
        'postal_area',
        # string Postal area
        'postcode',
        # string Postcode
        'owning_company',
        'resignation_date',
        'secretary',
    ]
