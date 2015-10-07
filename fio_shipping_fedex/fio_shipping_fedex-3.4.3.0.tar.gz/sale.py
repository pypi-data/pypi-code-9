# -*- coding: utf-8 -*-
"""
    sale.py

"""
from decimal import Decimal

from trytond.model import fields, ModelView
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction

from fedex.services.rate_service import FedexRateServiceRequest
from fedex.base_service import FedexError

__all__ = ['Configuration', 'Sale']
__metaclass__ = PoolMeta


class Configuration:
    'Sale Configuration'
    __name__ = 'sale.configuration'

    fedex_drop_off_type = fields.Many2One(
        'fedex.shipment.method', 'Default Drop-Off Type',
        domain=[('method_type', '=', 'dropoff')],
    )
    fedex_packaging_type = fields.Many2One(
        'fedex.shipment.method', 'Default Packaging Type',
        domain=[('method_type', '=', 'packaging')],
    )
    fedex_service_type = fields.Many2One(
        'fedex.shipment.method', 'Default Service Type',
        domain=[('method_type', '=', 'service')],
    )


class Sale:
    "Sale"
    __name__ = 'sale.sale'

    is_fedex_shipping = fields.Function(
        fields.Boolean('Is Fedex Shipping'),
        'get_is_fedex_shipping',
    )
    fedex_drop_off_type = fields.Many2One(
        'fedex.shipment.method', 'Default Drop-Off Type',
        domain=[('method_type', '=', 'dropoff')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': ~Eval('state').in_(['draft', 'quotation']),
        },
        depends=['is_fedex_shipping', 'state']
    )
    fedex_packaging_type = fields.Many2One(
        'fedex.shipment.method', 'Default Packaging Type',
        domain=[('method_type', '=', 'packaging')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': ~Eval('state').in_(['draft', 'quotation']),
        },
        depends=['is_fedex_shipping', 'state']
    )
    fedex_service_type = fields.Many2One(
        'fedex.shipment.method', 'Default Service Type',
        domain=[('method_type', '=', 'service')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': ~Eval('state').in_(['draft', 'quotation']),
        },
        depends=['is_fedex_shipping', 'state']
    )

    def get_is_fedex_shipping(self, name):
        return self.carrier and \
            self.carrier.carrier_cost_method == 'fedex' or False

    @classmethod
    def __setup__(self):
        super(Sale, self).__setup__()
        self._error_messages.update({
            'fedex_settings_missing': 'FedEx settings on this sale are missing',
            'fedex_rates_error':
                "Error while getting rates from Fedex: \n\n%s"
        })
        self._buttons.update({
            'update_fedex_shipment_cost': {
                'invisible': Eval('state') != 'quotation'
            }
        })

    def on_change_carrier(self):
        """
        Show/Hide UPS Tab in view on change of carrier
        """
        res = super(Sale, self).on_change_carrier()

        res['is_fedex_shipping'] = self.carrier and \
            self.carrier.carrier_cost_method == 'fedex'

        return res

    @staticmethod
    def default_fedex_drop_off_type():
        Config = Pool().get('sale.configuration')

        config = Config(1)
        return config.fedex_drop_off_type and config.fedex_drop_off_type.id

    @staticmethod
    def default_fedex_packaging_type():
        Config = Pool().get('sale.configuration')

        config = Config(1)
        return config.fedex_packaging_type and config.fedex_packaging_type.id

    @staticmethod
    def default_fedex_service_type():
        Config = Pool().get('sale.configuration')

        config = Config(1)
        return config.fedex_service_type and config.fedex_service_type.id

    def _get_carrier_context(self):
        "Pass sale in the context"
        # XXX: This override should not be here, it should be in
        # trytond-shipping

        context = super(Sale, self)._get_carrier_context()

        if not self.carrier.carrier_cost_method == 'fedex':
            return context

        context = context.copy()
        context['sale'] = self.id
        return context

    def on_change_lines(self):
        """Pass a flag in context which indicates the get_sale_price method
        of FedEx carrier not to calculate cost on each line change
        """
        with Transaction().set_context({'ignore_carrier_computation': True}):
            return super(Sale, self).on_change_lines()

    def apply_fedex_shipping(self):
        "Add a shipping line to sale for fedex"
        Currency = Pool().get('currency.currency')

        if self.is_fedex_shipping:
            with Transaction().set_context(self._get_carrier_context()):
                shipment_cost, currency_id = self.carrier.get_sale_price()
                if not shipment_cost:
                    return
            # Convert the shipping cost to sale currency from USD
            shipment_cost = Currency.compute(
                Currency(currency_id), shipment_cost, self.currency
            )
            self.add_shipping_line(
                shipment_cost,
                "%s - %s" % (
                    self.carrier.party.name, self.fedex_packaging_type.name
                )
            )

    @classmethod
    def quote(cls, sales):
        res = super(Sale, cls).quote(sales)
        cls.update_fedex_shipment_cost(sales)
        return res

    @classmethod
    @ModelView.button
    def update_fedex_shipment_cost(cls, sales):
        for sale in sales:
            sale.apply_fedex_shipping()

    def get_fedex_shipping_cost(self):
        """Returns the calculated shipping cost as sent by fedex
        :returns: The shipping cost
        """
        ProductUom = Pool().get('product.uom')

        fedex_credentials = self.carrier.get_fedex_credentials()

        if not all([
            self.fedex_drop_off_type, self.fedex_packaging_type,
            self.fedex_service_type
        ]):
            self.raise_user_error('fedex_settings_missing')

        rate_request = FedexRateServiceRequest(fedex_credentials)
        rate_request.RequestedShipment.DropoffType = self.fedex_drop_off_type.value
        rate_request.RequestedShipment.ServiceType = self.fedex_service_type.value
        rate_request.RequestedShipment.PackagingType = self.fedex_packaging_type.value
        rate_request.RequestedShipment.RateRequestTypes = "PREFERRED"
        rate_request.RequestedShipment.PreferredCurrency = self.currency.code

        # Shipper's address
        shipper_address = self._get_ship_from_address()
        rate_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        rate_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        rate_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient address
        rate_request.RequestedShipment.Recipient.Address.PostalCode = self.shipment_address.zip
        rate_request.RequestedShipment.Recipient.Address.CountryCode = self.shipment_address.country.code

        # Include estimated duties and taxes in rate quote, can be ALL or NONE
        rate_request.RequestedShipment.EdtRequestType = 'NONE'

        # Who pays for the rate_request?
        # RECIPIENT, SENDER or THIRD_PARTY
        rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = \
            'SENDER'

        weight_uom, = ProductUom.search([('symbol', '=', 'lb')])

        package_weight = rate_request.create_wsdl_object_of_type('Weight')
        package_weight.Value = float("%.2f" % self._get_total_weight(weight_uom))
        package_weight.Units = "LB"
        package = rate_request.create_wsdl_object_of_type('RequestedPackageLineItem')
        package.Weight = package_weight
        # Can be other values this is probably the most common
        package.PhysicalPackaging = 'BOX'
        package.GroupPackageCount = 1

        rate_request.add_package(package)

        try:
            rate_request.send_request()
        except FedexError, error:
            self.raise_user_error("fedex_rates_error", error_args=(error, ))

        for rate_detail in rate_request.response.RateReplyDetails[0].RatedShipmentDetails:
            if rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Currency != self.currency.code:
                continue
            return Decimal(rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Amount), self.currency.id

    def create_shipment(self, shipment_type):
        Shipment = Pool().get('stock.shipment.out')

        with Transaction().set_context(ignore_carrier_computation=True):
            shipments = super(Sale, self).create_shipment(shipment_type)

        if shipment_type == 'out' and shipments and self.is_fedex_shipping:
            Shipment.write(shipments, {
                'fedex_drop_off_type': self.fedex_drop_off_type.id,
                'fedex_packaging_type': self.fedex_packaging_type.id,
                'fedex_service_type': self.fedex_service_type.id,
            })
        return shipments
