from __future__ import unicode_literals

from ... import ProResource


class BankAccount(ProResource):
    attribute_names = [
        'bank',
        # string Name of bank
        'sortCode',
        # string Bank sort code
        'count',
        # integer Number of accounts
        'id',
        # string Identifier for bank account
    ]
