# -*- coding: utf-8 -*-

from cubicweb.entities import AnyEntity

class ShoppingCart(AnyEntity):
    """shopping cart"""
    __regid__ = 'ShoppingCart'

    @property
    def total(self):
        amount_taxes = 0
        amount = 0
        for item in self.reverse_in_cart:
            amount_taxes += item.taxes
            amount += item.price
        return amount, amount_taxes

class ShoppingItem(AnyEntity):
    """shopping items"""
    __regid__ = 'ShoppingItem'

    def dc_title(self):
        return u'%s %s' % (self.quantity, self.item.dc_title())

    @property
    def unit_price(self):
        return self.item.price

    @property
    def price(self):
        return self.item.price * self.quantity

    @property
    def taxes(self):
        return self.item.taxes * self.quantity

    @property
    def item(self):
        return self.item_type[0]

class ShoppingItemType(AnyEntity):
    """shopping items"""
    __regid__ = 'ShoppingItemType'

    def dc_title(self):
        return self._cw._(u'%(title)s (%(price)s currency per unit)') % {
            'title': self.title, 'price': self.price}
