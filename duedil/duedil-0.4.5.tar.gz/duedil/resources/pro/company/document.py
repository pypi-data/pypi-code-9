from __future__ import unicode_literals

from ... import ProResource


class Document(ProResource):
    attribute_names = [
        'id',
        # string Document ID
        'last_update',
        # dateTime Date of last update
        'documentCode',
        # string Document code
        'date',
        # string Date filed
        'description',
        # string Description of Document Filing
    ]
