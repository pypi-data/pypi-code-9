from __future__ import unicode_literals

from ... import ProResource


class Shareholder(ProResource):
    attribute_names = [
        'id',
        # string The registered ID of the company
        'last_update',
        # dateTime Date of last update
        'company',
        # string Company
        'title',
        # string Shareholders title
        'forename',
        # string Shareholders forename
        'surname',
        # string Shareholders surname
        'address1',
        # string Address 1
        'address2',
        # string Address 2
        'address3',
        # string Address 3
        'address4',
        # string Address 4
        'address5',
        # string Address 5
        'type',
        # string Type & class of the shares held
        'number',
        # integer The number of this type of share held
        'value',
        # integer The value of each share of this type held
        'currency',
        # string Currency
    ]
