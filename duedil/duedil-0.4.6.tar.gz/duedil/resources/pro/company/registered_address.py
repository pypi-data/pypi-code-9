from __future__ import unicode_literals

from ... import ProResource


class RegisteredAddress(ProResource):
    attribute_names = [
        # 'id',
        # string The registered ID of the company
        'last_update',
        # dateTime Date of last update
        'company',
        # string Company registration number
        'address1',
        # string Address part 1
        'address2',
        # string Address part 2
        'address3',
        # string Address part 3
        'address4',
        # string Address part 4
        'postcode',
        # string Postcode
        'phone',
        # string phone number
        'tps',
        # string TPS
        'website',
        # string Website
        'po_box',
        # string PO box number
        'care_of',
        # string Care of
        'email',
        # string Email address
        'area_code',
        # string Area code
    ]
