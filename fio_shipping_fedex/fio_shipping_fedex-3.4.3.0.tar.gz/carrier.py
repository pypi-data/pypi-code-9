# -*- coding: utf-8 -*-
"""
    carrier.py

"""
from decimal import Decimal

from trytond.pool import PoolMeta, Pool
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval
from fedex.config import FedexConfig


REQUIRED_IF_FEDEX = {
    'required': Eval('carrier_cost_method') == 'fedex',
}

__all__ = ['Carrier', 'FedexShipmentMethod']
__metaclass__ = PoolMeta


class FedexShipmentMethod(ModelSQL, ModelView):
    "FedEx Shipment methods"
    __name__ = 'fedex.shipment.method'

    name = fields.Char('Name', required=True, select=True)
    value = fields.Char('Value', required=True, select=True)
    method_type = fields.Selection([
        ('dropoff', 'Drop Off Type'),
        ('packaging', 'Packaging Type'),
        ('service', 'Service Type'),
    ], 'Type', required=True, select=True)


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    fedex_key = fields.Char('Key', states=REQUIRED_IF_FEDEX)
    fedex_password = fields.Char('Password', states=REQUIRED_IF_FEDEX)
    fedex_account_number = fields.Char(
        'Account Number', states=REQUIRED_IF_FEDEX
    )
    fedex_meter_number = fields.Char('Meter Number', states=REQUIRED_IF_FEDEX)
    fedex_is_test = fields.Boolean('Is Test Account?')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('fedex', 'FedEx')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

        cls._error_messages.update({
            'fedex_settings_missing': 'FedEx settings are incomplete',
        })

    def get_fedex_credentials(self):
        """
        Returns the fedex account credentials in tuple
        :return: FedexConfig object
        """
        if not all([
            self.fedex_key, self.fedex_account_number,
            self.fedex_password, self.fedex_meter_number,
        ]):
            self.raise_user_error('fedex_settings_missing')

        return FedexConfig(
            key=self.fedex_key,
            password=self.fedex_password,
            account_number=self.fedex_account_number,
            meter_number=self.fedex_meter_number,
            use_test_server=self.fedex_is_test
        )

    def get_sale_price(self):
        """Estimates the shipment rate for the current shipment
        The get_sale_price implementation by tryton's carrier module
        returns a tuple of (value, currency_id)
        :returns: A tuple of (value, currency_id)
        """
        Sale = Pool().get('sale.sale')
        Shipment = Pool().get('stock.shipment.out')
        Company = Pool().get('company.company')

        sale = Transaction().context.get('sale')
        shipment = Transaction().context.get('shipment')
        company = Company(Transaction().context.get('company'))

        if Transaction().context.get('ignore_carrier_computation'):
            return Decimal('0'), company.currency.id
        if not sale and not shipment:
            return Decimal('0'), company.currency.id

        if self.carrier_cost_method != 'fedex':
            return super(Carrier, self).get_sale_price()

        if sale:
            return Sale(sale).get_fedex_shipping_cost()
        if shipment:
            return Shipment(shipment).get_fedex_shipping_cost()

        return Decimal('0'), company.currency.id
