# coding=utf-8
__author__ = 'yalnazov'
from jsonobject import *
from . import shopping_cart_item

class ShoppingCart(JsonObject):
        items = ListProperty(shopping_cart_item.ShoppingCartItem)
