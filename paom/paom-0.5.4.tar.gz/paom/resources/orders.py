from paom.base import BaseResource


class Orders(BaseResource):

    ABSOLUTE_URL = "/orders/"
    REQUEST_TYPES = ["GET", "POST", "ALL", "PATCH", "DELETE"]


class Carts(BaseResource):

    ABSOLUTE_URL = "/cart/"


class CartItems(BaseResource):

    ABSOLUTE_URL = "/cart-items/"
    REQUEST_TYPES = ["GET", "POST", "PATCH", "DELETE"]
