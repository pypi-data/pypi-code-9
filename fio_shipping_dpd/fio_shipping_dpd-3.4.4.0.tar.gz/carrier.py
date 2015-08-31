# -*- coding: utf-8 -*-
"""
    carrier

"""
from decimal import Decimal
from suds import WebFault
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.model import fields, ModelView
from trytond.pyson import Eval
from trytond.wizard import Wizard, StateView, Button
from dpd_client import DPDClient

__all__ = ['Carrier', 'TestConnectionStart', 'TestConnection']
__metaclass__ = PoolMeta


STATES = {
    'required': Eval('carrier_cost_method') == 'dpd',
    'invisible': Eval('carrier_cost_method') != 'dpd'
}


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    dpd_url = fields.Char(
        'Base URL', help="Ex. https://public-ws-stage.dpd.com",
        states=STATES, depends=['carrier_cost_method']
    )
    dpd_login_service_wsdl = fields.Char(
        'Login Service URL', states=STATES, depends=['carrier_cost_method']
    )
    dpd_shipment_service_wsdl = fields.Char(
        'Shipment Service URL', states=STATES, depends=['carrier_cost_method']
    )
    dpd_depot_data_service_wsdl = fields.Char(
        'Depot Data Service URL', states=STATES, depends=['carrier_cost_method']
    )
    dpd_parcel_shop_finder_service_wsdl = fields.Char(
        'Parcel Shop Finder Service URL', states=STATES,
        depends=['carrier_cost_method']
    )
    dpd_username = fields.Char(
        'Username/DelisID', states=STATES, depends=['carrier_cost_method']
    )
    dpd_password = fields.Char(
        'Password', states=STATES, depends=['carrier_cost_method']
    )
    dpd_depot = fields.Char(
        'Depot', states=STATES, depends=['carrier_cost_method']
    )

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('dpd', 'DPD')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

        cls._buttons.update({
            'test_dpd_credentials': {},
        })

    @fields.depends('carrier_cost_method', 'dpd_url')
    def on_change_dpd_url(self):
        """
        Set the login_service and shipment_service URL on change of dpd_url
        """
        if self.carrier_cost_method != 'dpd':
            return {}
        if not self.dpd_url:
            return {}
        return {
            'dpd_login_service_wsdl': (
                self.dpd_url + '/services/LoginService/V2_0?wsdl'),
            'dpd_shipment_service_wsdl': (
                self.dpd_url + '/services/ShipmentService/V3_2?wsdl'),
            'dpd_depot_data_service_wsdl': (
                self.dpd_url + '/services/DepotDataService/V1_0?wsdl'),
            'dpd_parcel_shop_finder_service_wsdl': (
                self.dpd_url + '/services/DepotDataService/V1_0?wsdl'),
        }

    def get_dpd_client(self):
        """
        Return the DPD client with the username and password set
        """
        return DPDClient(
            self.dpd_login_service_wsdl,
            self.dpd_shipment_service_wsdl,
            self.dpd_depot_data_service_wsdl,
            self.dpd_parcel_shop_finder_service_wsdl,
            self.dpd_username,
            self.dpd_password,
            message_language=Transaction().context.get('language', 'en_US')
        )

    @classmethod
    @ModelView.button_action('shipping_dpd.wizard_test_connection')
    def test_dpd_credentials(cls, carriers):
        """
        Tests the connection. If there is a WebFault, raises an UserError
        """
        if len(carriers) != 1:
            cls.raise_user_error('Only one carrier can be tested at a time.')

        client = carriers[0].get_dpd_client()
        try:
            client.get_auth()
        except WebFault, exc:
            cls.raise_user_error(exc.fault)

    def get_sale_price(self):
        """Estimates the shipment rate for the current shipment
        DPD dont provide and shipping cost, so here shipping_cost will be 0
        returns a tuple of (value, currency_id)
        :returns: A tuple of (value, currency_id which in this case is USD)
        """
        Currency = Pool().get('currency.currency')
        Company = Pool().get('company.company')

        if self.carrier_cost_method != 'dpd':
            return super(Carrier, self).get_sale_price()  # pragma: no cover

        currency, = Currency.search([('code', '=', 'USD')])
        company = Transaction().context.get('company')

        if company:
            currency = Company(company).currency

        return Decimal('0'), currency.id


class TestConnectionStart(ModelView):
    "Test Connection"
    __name__ = 'shipping_dpd.wizard_test_connection.start'


class TestConnection(Wizard):
    """
    Test Connection Wizard
    """
    __name__ = 'shipping_dpd.wizard_test_connection'

    start = StateView(
        'shipping_dpd.wizard_test_connection.start',
        'shipping_dpd.wizard_test_connection_view_form',
        [
            Button('Ok', 'end', 'tryton-ok'),
        ]
    )
