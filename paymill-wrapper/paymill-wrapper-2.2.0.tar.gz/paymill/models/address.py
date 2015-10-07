# coding=utf-8
from jsonobject import *
__author__ = 'yalnazov'

class Address(JsonObject):

    name = StringProperty()
    """:type str: Name of recipient, max. 128 characters"""

    street_address = StringProperty()
    """:type str: Street address (incl. street number), max. 100 characters"""

    street_address_addition = StringProperty()
    """:type str: Addition to street address (e.g. building, floor, or c/o), max. 100 characters"""

    city = StringProperty()
    """:type str: City, max. 40 characters"""

    state = StringProperty()
    """:type str: State or province, max. 40 characters"""

    postal_code = StringProperty()
    """:type str: Country-specific postal code, max. 20 characters"""

    country = StringProperty()
    """:type str: 2-letter country code according to ISO 3166-1 alpha-2"""

    phone = StringProperty()
    """:type integer. Contact phone number, max. 20 characters"""
