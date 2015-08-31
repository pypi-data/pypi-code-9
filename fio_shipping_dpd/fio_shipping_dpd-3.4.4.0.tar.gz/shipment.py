# -*- coding: utf-8 -*-
"""
    shipping_dpd.py

"""
import base64
from dpd_client import DPDException
from trytond.pool import Pool, PoolMeta
from trytond.model import fields, ModelView
from trytond.pyson import Eval, Bool, And
from trytond.rpc import RPC
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, Button

__all__ = ['ShipmentOut', 'GenerateShippingLabel', 'ShippingDPD', 'Package']
__metaclass__ = PoolMeta


STATES = {
    'readonly': Eval('state') == 'done',
    'required': Bool(Eval('is_dpd_shipping')),
}

DPD_PRODUCTS = [
    (None, ''),
    ('CL', 'DPD CLASSIC'),
    ('E830', 'DPD 8:30'),
    ('E10', 'DPD 10:00'),
    ('E12', 'DPD 12:00'),
    ('E18', 'DPD 18:00'),
    ('IE2', 'DPD EXPRESS'),
    ('PL', 'DPD PARCELLetter'),
    ('PL+', 'DPD PARCELLetterPlus'),
    ('MAIL', 'DPD International Mail'),
]


class ShipmentOut:
    "Shipment Out"
    __name__ = 'stock.shipment.out'

    is_dpd_shipping = fields.Function(
        fields.Boolean('Is Shipping', readonly=True),
        'get_is_dpd_shipping'
    )

    dpd_product = fields.Selection(
        DPD_PRODUCTS, 'DPD Product', states=STATES, depends=[
            'state', 'is_dpd_shipping'
        ]
    )
    dpd_print_paper_format = fields.Selection(
        [
            ('A4', 'A4 (parcel label print)'),
            ('A6', 'A6 (parcel label print/direct printing)'),
        ], 'DPD Printer Paper Format', states=STATES, depends=[
            'state', 'is_dpd_shipping'
        ]
    )
    dpd_customs_terms = fields.Selection(
        [
            (None, ''),
            ('01', 'DAP, cleared'),
            ('02', 'DDP, delivered duty paid (incl. duties and excl. Taxes'),
            (
                '03',
                'DDP, delivered duty paid (incl duties and taxes) 05 = ex '
                'works (EXW)'
            ),
            ('06', 'DAP'),
        ], 'DPD customs terms', states={
            'readonly': Eval('state') == 'done',
            'invisible': ~Eval('is_international_shipping'),
            'required': And(
                Bool(Eval('is_dpd_shipping')),
                Bool(Eval('is_international_shipping'))
            ),
        }, depends=['state', 'is_international_shipping', 'is_dpd_shipping']
    )

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls.carrier.states = STATES
        cls.__rpc__.update({
            'make_dpd_labels': RPC(readonly=False, instantiate=0),
        })

    @staticmethod
    def default_dpd_print_paper_format():
        return 'A6'

    def get_is_dpd_shipping(self, name):
        """
        Check if shipping is from DPD
        """
        return self.carrier and self.carrier.carrier_cost_method == 'dpd'

    @fields.depends('is_dpd_shipping', 'carrier')
    def on_change_carrier(self):
        """
        Show/Hide DPD Tab in view on change of carrier
        """
        res = super(ShipmentOut, self).on_change_carrier()

        res['is_dpd_shipping'] = self.carrier and \
            self.carrier.carrier_cost_method == 'dpd'

        return res

    def _get_weight_uom(self):
        """
        Return uom for DPD
        """
        UOM = Pool().get('product.uom')
        if self.is_dpd_shipping:
            return UOM.search([('symbol', '=', 'g')])[0]
        return super(ShipmentOut, self)._get_weight_uom()

    def _get_dpd_general_shipment_data(self, dpd_client):
        """
        Returns a DPD shipment object
        """
        shipment_service_client = dpd_client.shipment_service_client

        general_shipment_data = shipment_service_client.factory.create(
            'ns0:generalShipmentData'
        )
        general_shipment_data.cUser = Transaction().user
        general_shipment_data.identificationNumber = self.code

        # TODO: fetch depot from API for consignment
        general_shipment_data.sendingDepot = self.carrier.dpd_depot

        general_shipment_data.mpsCustomerReferenceNumber1 = self.reference
        general_shipment_data.product = self.dpd_product

        # Weight should be rounded 10Gram units
        general_shipment_data.mpsWeight = int(round(self.weight / 10))

        from_address = self._get_ship_from_address()

        general_shipment_data.sender = from_address.to_dpd_address(
            shipment_service_client
        )
        general_shipment_data.recipient = self.delivery_address.to_dpd_address(
            shipment_service_client
        )
        return general_shipment_data

    def _get_dpd_product_and_service_data(self, dpd_client):
        """
        Returns a DPD productAndServiceData object
        """
        shipment_service_client = dpd_client.shipment_service_client

        product_and_service_data = shipment_service_client.factory.create(
            'ns0:productAndServiceData'
        )
        product_and_service_data.orderType = 'consignment'
        return product_and_service_data

    def _get_dpd_parcel_data(self, dpd_client):
        """
        Returns a DPD parcel object
        """
        shipment_service_client = dpd_client.shipment_service_client

        parcels = []
        for package in self.packages:
            parcel_data = shipment_service_client.factory.create(
                'ns0:parcel'
            )
            parcel_data.weight = int(round(package.weight / 10))
            parcel_data.customerReferenceNumber1 = package.code
            if self.is_international_shipping:
                # For international
                parcel_data.international = \
                    package._get_dpd_international_data(dpd_client)
            parcels.append(parcel_data)
        return parcels

    def _get_dpd_print_options(self, dpd_client):
        """
        Returns a DPD printOptions object
        """
        shipment_service_client = dpd_client.shipment_service_client

        # Set the printing options
        # TODO: This should be configurable
        print_options = shipment_service_client.factory.create(
            'ns0:printOptions')
        print_options.printerLanguage = 'PDF'
        print_options.paperFormat = self.dpd_print_paper_format
        print_options.startPosition = 'UPPER_LEFT'

        return print_options

    def make_dpd_labels(self):
        """
        Make labels for the shipment using DPD

        :return: Tracking number as string
        """
        Attachment = Pool().get('ir.attachment')

        if self.state not in ('packed', 'done'):
            self.raise_user_error('invalid_state')

        if not self.is_dpd_shipping:
            self.raise_user_error('wrong_carrier', 'DPD')

        if self.tracking_number:
            self.raise_user_error('tracking_number_already_present')

        if not self.packages:
            self.raise_user_error("no_packages", error_args=(self.id,))

        client = self.carrier.get_dpd_client()

        print_options = self._get_dpd_print_options(client)

        shipment_service_data = client.shipment_service_client.factory.create(
            'ns0:shipmentServiceData'
        )
        shipment_service_data.generalShipmentData = \
            self._get_dpd_general_shipment_data(client)

        shipment_service_data.productAndServiceData = \
            self._get_dpd_product_and_service_data(client)

        shipment_service_data.parcels = \
            self._get_dpd_parcel_data(client)

        # XXX: Not sure if parcel is needed here
        try:
            response = client.store_orders(
                print_options, [shipment_service_data]
            )
        except DPDException, exc:
            self.raise_user_error(exc.message)

        shipment_data, = response.shipmentResponses
        if hasattr(shipment_data, 'faults'):
            fault = shipment_data.faults[0]
            self.raise_user_error('%s: %s' % (fault.faultCode, fault.message))

        # DPD provides a different tracking number/parcel label number for
        # each parcel/package and sends them as response in the order of
        # which the parcels were sent in request
        for package, package_info in zip(
                self.packages, shipment_data.parcelInformation):
            package.tracking_number = package_info.parcelLabelNumber
            package.save()

        # Setting the tracking number of first package/parcel on the
        # shipment record
        tracking_number = self.packages[0].tracking_number
        self.__class__.write([self], {
            'tracking_number': unicode(tracking_number),
        })
        Attachment.create([{
            'name': "%s_%s.pdf" % (
                shipment_data.mpsId,
                shipment_data.identificationNumber
            ),
            'data': buffer(base64.decodestring(
                response.parcellabelsPDF
            )),
            'resource': '%s,%s' % (self.__name__, self.id)
        }])
        return tracking_number


class GenerateShippingLabel(Wizard):
    'Generate Labels'
    __name__ = 'shipping.label'

    dpd_config = StateView(
        'shipping.label.dpd',
        'shipping_dpd.shipping_dpd_config_wizard_view_form',
        [
            Button('Back', 'start', 'tryton-go-previous'),
            Button('Continue', 'generate', 'tryton-go-next'),
        ]
    )

    def default_dpd_config(self, data):
        shipment = self.start.shipment

        return {
            'dpd_product': shipment.dpd_product,
            'dpd_print_paper_format': shipment.dpd_print_paper_format,
            'dpd_customs_terms': shipment.dpd_customs_terms,
            'is_international_shipping': shipment.is_international_shipping,
        }

    def transition_next(self):
        state = super(GenerateShippingLabel, self).transition_next()

        if self.start.carrier.carrier_cost_method == 'dpd':
            return 'dpd_config'
        return state

    def update_shipment(self):
        shipment = super(GenerateShippingLabel, self).update_shipment()

        if self.start.carrier.carrier_cost_method == 'dpd':
            shipment.dpd_product = self.dpd_config.dpd_product
            shipment.dpd_customs_terms = self.dpd_config.dpd_customs_terms
            shipment.dpd_print_paper_format = \
                self.dpd_config.dpd_print_paper_format

        return shipment


class ShippingDPD(ModelView):
    'Generate Labels'
    __name__ = 'shipping.label.dpd'

    dpd_product = fields.Selection(
        DPD_PRODUCTS, 'DPD Product', required=True
    )
    dpd_print_paper_format = fields.Selection(
        [
            ('A4', 'A4 (parcel label print)'),
            ('A6', 'A6 (parcel label print/direct printing)'),
        ], 'DPD Printer Paper Format', required=True
    )
    is_international_shipping = fields.Boolean("Is International Shipping")
    dpd_customs_terms = fields.Selection(
        [
            (None, ''),
            ('01', 'DAP, cleared'),
            ('02', 'DDP, delivered duty paid (incl. duties and excl. Taxes'),
            (
                '03',
                'DDP, delivered duty paid (incl duties and taxes) 05 = ex '
                'works (EXW)'
            ),
            ('06', 'DAP'),
        ], 'DPD customs terms', states={
            'invisible': ~Eval('is_international_shipping')
        }, depends=['is_international_shipping']
    )


class Package:
    __name__ = 'stock.package'

    def _get_dpd_international_data(self, dpd_client):
        """
        Returns a DPD international object
        """
        shipment_service_client = dpd_client.shipment_service_client

        international_data = shipment_service_client.factory.create(
            'ns0:international'
        )
        value = 0
        customs_desc = []

        for move in self.moves:
            if move.quantity <= 0:
                continue
            value += float(move.product.customs_value_used) * move.quantity
            customs_desc.append(move.product.name)

        international_data.parcelType = False
        # DPD expects the customs amount in total without decimal separator
        # (e.g. 14.00 = 1400)
        international_data.customsAmount = int(value * 100)
        international_data.customsCurrency = self.shipment.cost_currency.code
        international_data.customsTerms = self.shipment.dpd_customs_terms
        international_data.customsContent = ', '.join(customs_desc[:35])
        international_data.commercialInvoiceConsignee = \
            self.shipment.delivery_address.to_dpd_address(
                shipment_service_client)
        return international_data
