from django.conf import settings
from django.contrib import messages
from django import dispatch
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from changer.c5.shoppingcart.models import Cart, Item


def import_object(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise Exception('Error importing request processor module %s: "%s"' % (module, e))
    try:
        klass = getattr(mod, attr)
    except AttributeError, e:
        raise Exception('Module "%s" does not define a "%s" callable request processor' % (module, attr))
    return klass


ID_KEY = getattr(settings,
    'SHOPPINGCART_ID_KEY',
    'changer_cartid')
REDIRECT_TO = getattr(settings,
    'SHOPPINGCART_REDIRECT_TO',
    '/')
FAIL = getattr(settings,
    'SHOPPINGCART_FAIL',
    _(u'Something went wrong. The product was not added to your shopping cart.'))
QUANTITY_FIELDNAME = getattr(settings,
    'SHOPPINGCART_QUANTITY_FIELDNAME',
    'quantity')
PRODUCT_FIELDNAME = getattr(settings,
    'SHOPPINGCART_PRODUCT_FIELDNAME',
    'product')
PRODUCT_CLASSNAME = import_object(getattr(settings,
    'SHOPPINGCART_PRODUCT_CLASSNAME'))

REDIRECT_AFTER_CHECKOUT = getattr(settings,
    'SHOPPINGCART_REDIRECT_AFTER_CHECKOUT')
SUCCESS_MSG = getattr(settings, 
    'SHOPPINGCART_SUCCESS_MSG',
    _(u'Your request has been sent, you will receive an invoice from us shortly'))

cart_checkout_signal = dispatch.Signal(providing_args=["cart", "request"])

class SessionCart(object):

    def __init__(self, request):
        cart_id = request.session.get(ID_KEY)
        self.request = request
    
        if cart_id:
            #logging.debug('cart id: %s' % cart_id)
            try:
                cart = Cart.objects.get(
                    pk=cart_id,
                    checked_out=False,
                )
            except Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)

        self.cart = cart

    def new(self, request):
        cart = Cart.objects.create()
        request.session[ID_KEY] = cart.id
        return cart

    def add(self, request, product, unit_price, quantity=1):
        try:
            Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except Item.DoesNotExist:
            Item.objects.create(
                cart=self.cart,
                quantity=quantity,
                unit_price=unit_price,
                content_object=product,
            )
            messages.add_message(request, messages.SUCCESS, _(u'Product added to shopping cart'))
            #Product aan winkelmandje toegevoegd'))
        else:
            messages.add_message(request, messages.WARNING, _(u'This product is already in your shopping cart'))
            #Dit product is al in het winkelmandje'))

    def remove(self, product):
        try:
            item = Item.objects.get(
                cart=self.cart,
                content_object=product)
        except Item.DoesNotExist:
            raise Item.DoesNotExist
        else:
            item.delete()

    def clear(self):
        for item in self.cart.items.all():
            item.delete()
        self.request.session[ID_KEY] = ''

    @property
    def count(self):
        count = 0
        for item in self.cart.items.all():
            count += item.quantity
        return count
