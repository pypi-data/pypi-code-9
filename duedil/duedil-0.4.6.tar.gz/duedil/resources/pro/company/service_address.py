from __future__ import unicode_literals

from ... import ProResource


class ServiceAddress(ProResource):
    attribute_names = [
        'id',
        # string
        'last_update',
        # dateTime Date of last update
        'address1',
        # string Address part 1
        'address2',
        # string Address part 2
        'address3',
        # string Address part 3
        'address4',
        # string Address part 4
        'address5',
        # string Address part 5
        'postcode',
        # string Postcode
        'postal_area',
        # string Area code
    ]
