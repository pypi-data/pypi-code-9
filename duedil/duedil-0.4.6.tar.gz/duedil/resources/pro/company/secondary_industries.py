from __future__ import unicode_literals

from ... import ProResource


class Industry(ProResource):
    attribute_names = [
        'id',
        # string The registered ID of the company
        'sicCode',
        # string The additional SIC code the company has provided.
        'sicCodeDescription',
        # string Description of this SIC code.
    ]
