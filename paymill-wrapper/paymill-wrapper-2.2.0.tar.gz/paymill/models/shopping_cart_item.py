# coding=utf-8
from jsonobject import *
__author__ = 'yalnazov'

class ShoppingCartItem(JsonObject):

    name = StringProperty()
    """:type str: Item name, max. 127 characters"""

    description = StringProperty()
    """:type str: Additional description, max. 127 characters"""

    amount = IntegerProperty()
    """:type str: Price for a single item (including tax) Can be positive, zero, or negative (to represent a discount)"""

    quantity = IntegerProperty()
    """:type str: Quantity of this item"""

    item_number = StringProperty()
    """:type str: State or province, max. 40 characters"""

    postal_code = StringProperty()
    """:type str: Country-specific postal code, max. 20 characters"""

    country = StringProperty()
    """:type str: 2-letter country code according to ISO 3166-1 alpha-2"""

    phone = StringProperty()
    """:type integer. Contact phone number, max. 20 characters"""
