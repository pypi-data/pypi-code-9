# -*- coding: utf-8 -*-
"""
    checkout

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from itsdangerous import URLSafeSerializer, BadSignature

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.modules.nereid_checkout.checkout import not_empty_cart, \
    current_app, sale_has_non_guest_party
from nereid import route, redirect, url_for, render_template, request, flash, \
    abort

__metaclass__ = PoolMeta
__all__ = ['Checkout']


class Checkout:
    __name__ = 'nereid.checkout'

    @classmethod
    @route('/checkout/delivery-method', methods=['GET', 'POST'])
    @not_empty_cart
    @sale_has_non_guest_party
    def delivery_method(cls):
        '''
        Selection of delivery method (options)
        Based on the shipping address selected, the delivery options
        could be shown to the user. This may include choosing shipping speed
        and if there are multiple items, the option to choose items as they are
        available or all at once.
        '''
        NereidCart = Pool().get('nereid.cart')
        Carrier = Pool().get('carrier')
        Sale = Pool().get('sale.sale')

        signer = URLSafeSerializer(current_app.config['SECRET_KEY'])

        cart_sale = NereidCart.open_cart().sale

        if not cart_sale.shipment_address:
            return redirect(url_for('nereid.checkout.shipping_address'))

        if not cart_sale.package_weight:
            # No weight, no shipping. Have fun !
            return redirect(url_for('nereid.checkout.payment_method'))

        if request.method == 'POST' and \
                request.form.get('shipping_service_data'):
            try:
                shipping_service_data = signer.loads(
                    request.form.get('shipping_service_data'))
            except BadSignature:
                abort(400)
            Sale.write([cart_sale], shipping_service_data)
            cart_sale.apply_shipping()
            return redirect(url_for('nereid.checkout.payment_method'))

        shipping_overweight = False
        delivery_rates = []
        with Transaction().set_context(sale=cart_sale.id):
            try:
                delivery_rates = Carrier.get_rate_list()
            except UserError, e:
                # Possible Errors: Overweighted shipment, Invalid address
                # TODO: Handle gracefully
                flash(e.message)
                return redirect(url_for('nereid.checkout.shipping_address'))

        # Sign write_vals before feeding to template
        signed_rates = []
        for rate in delivery_rates:
            signed_rates.append(rate[:4] + (signer.dumps(rate[4]),))

        return render_template(
            'checkout/delivery_method.jinja', sale=cart_sale,
            delivery_rates=signed_rates, shipping_overweight=shipping_overweight
        )
