from __future__ import unicode_literals

from ... import ProResource


class Mortgage(ProResource):
    attribute_names = [
        'id',
        # string Mortgage ID
        'last_update',
        # dateTime Date last updated
        'number',
        # integer Number of charge
        'date_created',
        # dateTime Date created
        'type',
        # string Type of charge
        'date_registered',
        # dateTime Date registered
        'persons_entitled',
        # string Persons entitled
        'date_satisfied',
        # dateTime Date satisfied
        'status',
        # string Status
        'details',
        # string Details
        'amount_secured',
        # string Amount secured
    ]
