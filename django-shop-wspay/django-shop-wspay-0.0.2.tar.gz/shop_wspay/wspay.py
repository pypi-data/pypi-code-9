# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.contrib.syndication.views import add_domain

from shop.models import Cart
from shop.models.ordermodel import Order
from shop.util.decorators import on_method, shop_login_required, order_required
from shop.order_signals import cancelled

from shop_wspay.forms import WSPayForm
from shop_wspay import settings as sws


class WSPayBackend(object):
    url_namespace = 'wspay'
    backend_name = 'WSPay'
    backend_verbose_name = _('WSPay')

    def __init__(self, shop):
        self.shop = shop

    @on_method(shop_login_required)
    @on_method(order_required)
    def pay(self, request):
        shop = self.shop
        order = shop.get_order(request)
        order.status = Order.CONFIRMED
        order.save()
        site = get_current_site(request)
        site_url = add_domain(site.domain, '', request.is_secure())
        order_id = shop.get_order_unique_id(order)
        order_total = shop.get_order_total(order)

        # Split the order total by a decimal point and remove all dots
        # and commas that might be used in a tousand separator.
        total_amount = '{:.2f}'.format(order_total).rsplit('.', 1)
        total_amount[0] = total_amount[0].replace(',', '').replace('.', '')
        signature_total_amount = ''.join(total_amount)

        # Add a comma as a decimal separator.
        total_amount = ','.join(total_amount)

        signature_str = '{shop_id}{secret_key}{shopping_cart_id}{secret_key}'\
            '{total_amount}{secret_key}'.format(
                shop_id=sws.SHOP_ID, secret_key=sws.SECRET_KEY,
                shopping_cart_id=order_id, total_amount=signature_total_amount)

        signature = hashlib.md5()
        signature.update(signature_str)
        signature = signature.hexdigest()

        data = {
            'ShopID': sws.SHOP_ID,
            'ShoppingCartID': order_id,
            'TotalAmount': total_amount,
            'Signature': signature,
            'ReturnURL': site_url + reverse('wspay-verify'),
            'CancelURL': site_url + reverse('wspay-cancel'),
            'ReturnErrorURL': site_url + reverse('wspay-error'),
        }

        form = WSPayForm(initial=data)
        return render(request, 'shop_wspay/pay.html', {
            'form': form,
            'form_url': sws.FORM_URL,
            'order': order,
        })

    @on_method(shop_login_required)
    @on_method(order_required)
    def verify(self, request):
        shop = self.shop
        order = shop.get_order(request)
        order_name = shop.get_order_short_name(order)
        order_id = shop.get_order_unique_id(order)
        order_total = shop.get_order_total(order)

        data = {
            'ShoppingCartID': int(request.GET.get('ShoppingCartID', 0)),
            'Success': int(request.GET.get('Success', 0)),
            'ApprovalCode': request.GET.get('ApprovalCode', ''),
            'Signature': request.GET.get('Signature', ''),
        }

        signature_str = '{shop_id}{secret_key}{shopping_cart_id}{secret_key}'\
            '{success}{secret_key}{approval_code}{secret_key}'.format(
                shop_id=sws.SHOP_ID, secret_key=sws.SECRET_KEY,
                shopping_cart_id=data['ShoppingCartID'],
                success=data['Success'], approval_code=data['ApprovalCode'])

        signature = hashlib.md5()
        signature.update(signature_str)
        signature = signature.hexdigest()

        # Check if transaction failed.
        if (data['ShoppingCartID'] != order_id or
                data['ApprovalCode'] == '' or
                data['Success'] != 1 or
                data['Signature'] != signature):
            return render(request, 'shop_wspay/failed.html', {
                'order': order,
                'order_name': order_name,
            })

        shop.confirm_payment(
            order, order_total, data['ApprovalCode'], self.backend_name)

        return HttpResponseRedirect(shop.get_finished_url())

    @on_method(shop_login_required)
    @on_method(order_required)
    def cancel(self, request):
        shop = self.shop
        order = shop.get_order(request)
        order_name = shop.get_order_short_name(order)
        order.status = Order.CANCELED
        order.save()

        # Empty the cart.
        try:
            cart = Cart.objects.get(pk=order.cart_pk)
            cart.empty()
        except Cart.DoesNotExist:
            pass

        cancelled.send(sender=self, order=order)
        return render(request, 'shop_wspay/cancel.html', {
            'order': order,
            'order_name': order_name,
        })

    @on_method(shop_login_required)
    @on_method(order_required)
    def error(self, request):
        shop = self.shop
        order = shop.get_order(request)
        order_name = shop.get_order_short_name(order)

        return render(request, 'shop_wspay/error.html', {
            'order': order,
            'order_name': order_name,
        })

    def get_urls(self):
        return patterns(
            '',
            url(r'^$', self.pay, name='wspay'),
            url(r'^verify/$', self.verify, name='wspay-verify'),
            url(r'^cancel/$', self.cancel, name='wspay-cancel'),
            url(r'^error/$', self.error, name='wspay-error'),
        )
