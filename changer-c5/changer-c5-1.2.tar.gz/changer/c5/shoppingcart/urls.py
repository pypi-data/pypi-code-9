from django.conf.urls import patterns, url

from changer.c5.shoppingcart import (PRODUCT_CLASSNAME,
                                     QUANTITY_FIELDNAME,
                                     PRODUCT_FIELDNAME)


urlpatterns = patterns('',

    url(r'^anonymous/?$',
       'changer.c5.shoppingcart.views.cart_get_customer_info',
       name="get-customer-info"),
    
    url(r'^checkout/?$',
        'changer.c5.shoppingcart.views.cart_checkout',
        name="cart-checkout"),
    
    url(r'^add/?$',
        'changer.c5.shoppingcart.views.cart_add',
        {'class_name': PRODUCT_CLASSNAME,
         'qty_field': QUANTITY_FIELDNAME,
         'product_field': PRODUCT_FIELDNAME},
        name="cart-add"),
    
    url(r'^view/?$',
        'changer.c5.shoppingcart.views.cart_view',
        name="cart-view"),
    
    url(r'^increase/(?P<item_id>.*)/?$',
        'changer.c5.shoppingcart.views.cart_increase',
        name="cart-increase"),
    
    url(r'^decrease/(?P<item_id>.*)/?$',
        'changer.c5.shoppingcart.views.cart_decrease',
        name="cart-decrease"),
    
    url(r'^remove/(?P<item_id>.*)/?$',
        'changer.c5.shoppingcart.views.cart_remove',
        name="cart-remove"),
)
