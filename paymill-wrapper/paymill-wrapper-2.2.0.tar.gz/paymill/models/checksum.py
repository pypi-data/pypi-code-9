# coding=utf-8
from jsonobject import *
__author__ = 'yalnazov'

class Checksum(JsonObject):

    id = StringProperty()
    """:type str: Unique identifier of this Checksum"""

    checksum = StringProperty()
    """:type str: Checksum value"""

    data = StringProperty()
    """:type str: URI encoded data which integrity is checked by the Checksum"""

    type = StringProperty()
    """:type str: Checksum type. Possible values=(paypal)"""

    action = StringProperty()
    """:type str: Checksum action. Possible values=(transaction, payment, null)"""

    app_id = StringProperty()
    """:type string or null. App (ID) that created this payment or null if created by yourself"""

    created_at = IntegerProperty()
    """:type integer: unix timestamp identifying time of creation"""

    updated_at = IntegerProperty()
    """:type integer. unix timestamp identifying time of last change"""
