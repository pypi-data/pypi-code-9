# coding=utf-8
from ..models.checksum import Checksum
from ..models.address import Address
from ..models.shopping_cart_item import ShoppingCartItem
from ..models.shopping_cart import ShoppingCart
from .paymill_service import PaymillService
import json
__author__ = 'yalnazov'


class ChecksumService(PaymillService):
    def endpoint_path(self):
        return '/checksums'

    def paymill_object(self):
        return Checksum

    def create(self, checksum_type, amount, currency, return_url, cancel_url, description=None, checksum_action='transaction',
               fee_amount=None, fee_payment=None, fee_currency=None, checkout_options=None, require_reusable_payment=None,
               reusable_payment_description=None, items=None, shipping_address=None, billing_address=None, app_id=None):
        """Creates new transaction/payment Checksum
        :param str checksum_type : Type of request verified by this checksum
        :param int amount: Amount (in cents) which will be charged
        :param str currency: ISO 4217 formatted currency code
        :param str return_url: The identifier of a client
        :param int cancel_url: Fee included in the transaction amount (set by a connected app).
        :param str description: A short description for the transaction
        :param str checksum_action: The identifier of the payment from which the fee will be charged
        :param int fee_amount: Fee included in the transaction amount (set by a connected app). Mandatory if fee_payment is set.
        :param str fee_payment: The identifier of the payment from which the fee will be charged (Payment object).

        :param str fee_currency: The currency of the fee (e.g. EUR, USD). If it´s not set, the currency of the transaction is used.
            We suggest to always use as it might cause problems, if your account does not support the same currencies as your merchants accounts.
        :param list checkout_options: Various options that determine behavior before/during/after checkout such as editability of address fields.
        :param boolean require_reusable_payment: Set this to true if you want to ask the buyer for a billing agreement during checkout.
            If the buyer accepts, the resulting payment can be reused for transactions and subscriptions without additional interaction.
        :param str reusable_payment_description: Description appears at the acquirers checkout page (e.g. PayPal) when you request permission for a reusable payment, max. 127 characters.
        :param list of ShoppingCartItem items: Shopping cart items purchased with this transaction.
        :param Address shipping_address: Billing address for this transaction.
        :param Address billing_address: Billing address for this transaction.
        :params str app_id: App (ID) that created this payment or null if created by yourself.
        :return Checksum: the created Checksum object
        """
        params = dict(checksum_type=checksum_type, amount=amount, currency=currency, return_url=return_url, cancel_url=cancel_url)

        if description is not None:
            params.update(description=description)

        if checksum_action is not None:
            params.update(checksum_action=checksum_action)

        if shipping_address is not None and isinstance(shipping_address, Address):
            params.update(shipping_address=str(shipping_address.to_json()))

        if billing_address is not None and isinstance(billing_address, Address):
            params.update(billing_address=str(billing_address.to_json()))

        if items is not None and isinstance(items, list) and len(items) > 0 and isinstance(items[0], ShoppingCartItem):
            params.update(items=str(ShoppingCart(items=items).to_json()))

        if fee_amount is not None:
            params.update(fee_amount=fee_amount)

        if fee_payment is not None:
            params.update(fee_payment=fee_payment)

        if fee_currency is not None:
            params.update(fee_currency=fee_currency)

        if checkout_options is not None and isinstance(checkout_options, dict):
            params.update(checkout_options=json.dumps(checkout_options))

        if app_id is not None:
            params.update(app_id=app_id)

        if reusable_payment_description is not None:
            params.update(reusable_payment_description=reusable_payment_description)

        if require_reusable_payment is not None:
            params.update(require_reusable_payment=require_reusable_payment)

        return self._create(params)

    def detail(self, obj):
        """Returns/refreshes the remote Subscription representation with that obj.id
        :param Subscription obj: the Subscription object with an id set
        :return Subscription: the fresh Subscription object
        """
        return self._detail(obj)
