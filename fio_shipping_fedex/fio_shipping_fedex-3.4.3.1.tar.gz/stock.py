# -*- coding: utf-8 -*-
"""
    stock.py

"""
from decimal import Decimal
import base64

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.rpc import RPC
from trytond.transaction import Transaction

from fedex.services.rate_service import FedexRateServiceRequest
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.base_service import FedexError

__all__ = [
    'ShipmentOut', 'GenerateShippingLabel',
]
__metaclass__ = PoolMeta


class ShipmentOut:
    "Shipment Out"
    __name__ = 'stock.shipment.out'

    is_fedex_shipping = fields.Function(
        fields.Boolean('Is Shipping', readonly=True),
        'get_is_fedex_shipping'
    )
    fedex_drop_off_type = fields.Many2One(
        'fedex.shipment.method', 'Default Drop-Off Type',
        domain=[('method_type', '=', 'dropoff')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': Eval('state') == 'done',
        },
        depends=['is_fedex_shipping', 'state']
    )
    fedex_packaging_type = fields.Many2One(
        'fedex.shipment.method', 'Default Packaging Type',
        domain=[('method_type', '=', 'packaging')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': Eval('state') == 'done',
        },
        depends=['is_fedex_shipping', 'state']
    )
    fedex_service_type = fields.Many2One(
        'fedex.shipment.method', 'Default Service Type',
        domain=[('method_type', '=', 'service')],
        states={
            'required': Eval('is_fedex_shipping', True),
            'readonly': Eval('state') == 'done',
        },
        depends=['is_fedex_shipping', 'state']
    )
    fedex_commercial_invoice_terms_of_sale = fields.Selection([
        ('CFR_OR_CPT', 'CFR_OR_CPT'),
        ('CIF_OR_CIP', 'CIF_OR_CIP'),
        ("DAP", "DAP"),
        ("DAT", "DAT"),
        ("DDP", "DDP"),
        ("DDU", "DDU"),
        ("EXW", "EXW"),
        ("FOB_OR_FCA", "FOB_OR_FCA"),
    ], "Terms of Sale", )

    @staticmethod
    def default_fedex_commercial_invoice_terms_of_sale():
        return "DDU"

    def get_is_fedex_shipping(self, name):
        """
        Check if shipping is from fedex
        """
        return self.carrier and \
            self.carrier.carrier_cost_method == 'fedex' or False

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

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        # There can be cases when people might want to use a different
        # shipment carrier after the shipment is marked as done
        cls.carrier.states = {
            'readonly': ~Eval('state').in_(['packed', 'done']),
        }
        cls._error_messages.update({
            'error_label': 'Error in generating label: \n\n%s',
            'fedex_settings_missing':
                'FedEx settings on this sale are missing',
            'tracking_number_already_present':
                'Tracking Number is already present for this shipment.',
            'invalid_state': 'Labels can only be generated when the '
                'shipment is in Packed or Done states only',
            'wrong_carrier': 'Carrier for selected shipment is not FedEx',
            'fedex_shipping_cost_error':
                'Error while getting shipping cost from Fedex: \n\n%s'
        })
        cls.__rpc__.update({
            'make_fedex_labels': RPC(readonly=False, instantiate=0),
            'get_fedex_shipping_cost': RPC(readonly=False, instantiate=0),
        })

    def on_change_carrier(self):
        with Transaction().set_context(ignore_carrier_computation=True):
            res = super(ShipmentOut, self).on_change_carrier()

        res['is_fedex_shipping'] = self.carrier and \
            self.carrier.carrier_cost_method == 'fedex'

        return res

    def _get_carrier_context(self):
        "Pass shipment in the context"
        context = super(ShipmentOut, self)._get_carrier_context()

        if not self.carrier.carrier_cost_method == 'fedex':
            return context

        context = context.copy()
        context['shipment'] = self.id
        return context

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
        rate_request.RequestedShipment.PreferredCurrency = self.cost_currency.code

        # Shipper's address
        shipper_address = self._get_ship_from_address()
        rate_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        rate_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        rate_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient address
        rate_request.RequestedShipment.Recipient.Address.PostalCode = self.delivery_address.zip
        rate_request.RequestedShipment.Recipient.Address.CountryCode = self.delivery_address.country.code

        # Include estimated duties and taxes in rate quote, can be ALL or NONE
        rate_request.RequestedShipment.EdtRequestType = 'NONE'

        # Who pays for the rate_request?
        # RECIPIENT, SENDER or THIRD_PARTY
        rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

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
            self.raise_user_error("fedex_shipping_cost_error", error_args=(error, ))

        for rate_detail in rate_request.response.RateReplyDetails[0].RatedShipmentDetails:
            if rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Currency != self.currency.code:
                continue
            return Decimal(rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Amount), self.currency.id

    def make_fedex_labels(self):
        """
        Make labels for the given shipment

        :return: Tracking number as string
        """
        Attachment = Pool().get('ir.attachment')
        Uom = Pool().get('product.uom')
        Company = Pool().get('company.company')

        if self.state not in ('packed', 'done'):
            self.raise_user_error('invalid_state')

        if not self.carrier.carrier_cost_method == 'fedex':
            self.raise_user_error('wrong_carrier')

        if self.tracking_number:
            self.raise_user_error('tracking_number_already_present')

        fedex_credentials = self.carrier.get_fedex_credentials()

        ship_request = FedexProcessShipmentRequest(fedex_credentials)
        ship_request.RequestedShipment.DropoffType = self.fedex_drop_off_type.value
        ship_request.RequestedShipment.ServiceType = self.fedex_service_type.value
        ship_request.RequestedShipment.PackagingType = self.fedex_packaging_type.value

        company = Company(Transaction().context.get('company'))
        shipper_address = self._get_ship_from_address()

        # Shipper contact info.
        ship_request.RequestedShipment.Shipper.Contact.PersonName = shipper_address.name
        ship_request.RequestedShipment.Shipper.Contact.CompanyName = company.party.name
        ship_request.RequestedShipment.Shipper.Contact.PhoneNumber = shipper_address.party.phone

        # Shipper address.
        ship_request.RequestedShipment.Shipper.Address.StreetLines = [
            shipper_address.street or '', shipper_address.streetbis or ''
        ]
        ship_request.RequestedShipment.Shipper.Address.City = shipper_address.city
        ship_request.RequestedShipment.Shipper.Address.StateOrProvinceCode = shipper_address.subdivision.code[-2:]
        ship_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        ship_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        ship_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient contact info.
        ship_request.RequestedShipment.Recipient.Contact.PersonName = self.customer.name
        ship_request.RequestedShipment.Recipient.Contact.PhoneNumber = self.customer.phone

        # Recipient address
        ship_request.RequestedShipment.Recipient.Address.StreetLines = [
            self.delivery_address.street or '',
            self.delivery_address.streetbis or ''
        ]
        ship_request.RequestedShipment.Recipient.Address.City = self.delivery_address.city
        ship_request.RequestedShipment.Recipient.Address.StateOrProvinceCode = self.delivery_address.subdivision.code[-2:]
        ship_request.RequestedShipment.Recipient.Address.PostalCode = self.delivery_address.zip
        ship_request.RequestedShipment.Recipient.Address.CountryCode = self.delivery_address.country.code

        # Preferred currency
        ship_request.RequestedShipment.RateRequestTypes = "PREFERRED"
        ship_request.RequestedShipment.PreferredCurrency = self.cost_currency.code

        # This is needed to ensure an accurate rate quote with the response.
        ship_request.RequestedShipment.Recipient.Address.Residential = True
        ship_request.RequestedShipment.EdtRequestType = 'NONE'

        ship_request.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = fedex_credentials.account_number
        ship_request.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.Contact = ship_request.RequestedShipment.Shipper.Contact

        ship_request.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'
        ship_request.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        ship_request.RequestedShipment.LabelSpecification.ImageType = 'PNG'
        ship_request.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        ship_request.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

        if self.is_international_shipping:
            self._set_fedex_customs_details(ship_request)

        uom_pound, = Uom.search([('symbol', '=', 'lb')])

        master_tracking_number = None
        ship_request.RequestedShipment.PackageCount = len(self.packages)
        ship_request.RequestedShipment.TotalWeight.Units = 'LB'
        ship_request.RequestedShipment.TotalWeight.Value = float("%.2f" % Uom.compute_qty(
            self.weight_uom, self.weight, uom_pound
        ))

        for index, package in enumerate(self.packages, start=1):
            if master_tracking_number is not None:
                tracking_id = ship_request.create_wsdl_object_of_type(
                    'TrackingId'
                )
                tracking_id.TrackingNumber = master_tracking_number
                tracking_id.TrackingIdType = 'EXPRESS'
                ship_request.RequestedShipment.MasterTrackingId = tracking_id

            package_weight = ship_request.create_wsdl_object_of_type('Weight')
            package_weight.Value = float("%.2f" % Uom.compute_qty(
                package.weight_uom, package.weight, uom_pound
            ))
            package_weight.Units = "LB"

            package_item = ship_request.create_wsdl_object_of_type('RequestedPackageLineItem')
            package_item.PhysicalPackaging = 'BOX'
            package_item.Weight = package_weight
            package_item.SequenceNumber = index
            ship_request.RequestedShipment.RequestedPackageLineItems = [package_item]

            try:
                ship_request.send_request()
            except FedexError, error:
                self.raise_user_error("error_label", error_args=(error, ))

            tracking_number = ship_request.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
            if index == 1:
                master_tracking_number = tracking_number

            package.tracking_number = tracking_number
            package.save()

            for id, image in enumerate(ship_request.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts):
                Attachment.create([{
                    'name': "%s_%s_Fedex.png" % (tracking_number, id),
                    'type': 'data',
                    'data': buffer(base64.decodestring(image.Image)),
                    'resource': '%s,%s' % (self.__name__, self.id)
                }])

        for rate_detail in ship_request.response.CompletedShipmentDetail.ShipmentRating.ShipmentRateDetails:
            if rate_detail.TotalNetFedExCharge.Currency != self.cost_currency.code:
                continue
            self.cost = Decimal(str(rate_detail.TotalNetFedExCharge.Amount))
            self.tracking_number = master_tracking_number
            self.save()

        return master_tracking_number

    def _set_fedex_customs_details(self, ship_request):
        """
        Computes the details of the customs items and passes to fedex request
        """
        ProductUom = Pool().get('product.uom')

        customs_detail = ship_request.create_wsdl_object_of_type(
            'CustomsClearanceDetail'
        )
        customs_detail.DocumentContent = 'DOCUMENTS_ONLY'
        customs_detail.__delattr__('FreightOnValue')
        customs_detail.__delattr__('ClearanceBrokerage')

        weight_uom, = ProductUom.search([('symbol', '=', 'lb')])

        from_address = self._get_ship_from_address()

        # Encoding Items for customs
        commodities = []
        customs_value = 0
        for move in self.outgoing_moves:
            if move.product.type == 'service':
                continue
            commodity = ship_request.create_wsdl_object_of_type('Commodity')
            commodity.NumberOfPieces = len(self.outgoing_moves)
            commodity.Name = move.product.name
            commodity.Description = move.product.description or \
                move.product.name
            commodity.CountryOfManufacture = from_address.country.code
            commodity.Weight.Units = 'LB'
            commodity.Weight.Value = float("%.2f" % move.get_weight(weight_uom))
            commodity.Quantity = int(move.quantity)
            commodity.QuantityUnits = 'EA'
            commodity.UnitPrice.Amount = move.unit_price.quantize(Decimal('.01'))
            commodity.UnitPrice.Currency = self.company.currency.code
            commodity.CustomsValue.Currency = self.company.currency.code
            commodity.CustomsValue.Amount = (Decimal(str(move.quantity)) * move.unit_price).quantize(Decimal('.01'))
            commodities.append(commodity)
            customs_value += Decimal(str(move.quantity)) * move.unit_price

        customs_detail.CustomsValue.Currency = self.company.currency.code
        customs_detail.CustomsValue.Amount = customs_value.quantize(Decimal('.01'))
        customs_detail.Commodities = commodities

        # Commercial Invoice
        customs_detail.CommercialInvoice.TaxesOrMiscellaneousChargeType = 'OTHER'
        customs_detail.CommercialInvoice.Purpose = "SAMPLE"
        customs_detail.CommercialInvoice.TermsOfSale = self.fedex_commercial_invoice_terms_of_sale
        customs_detail.DutiesPayment.PaymentType = 'SENDER'
        customs_detail.DutiesPayment.Payor = ship_request.RequestedShipment.ShippingChargesPayment.Payor

        ship_request.RequestedShipment.CustomsClearanceDetail = customs_detail


class GenerateShippingLabel:
    'Generate Labels'
    __name__ = 'shipping.label'

    def transition_next(self):
        state = super(GenerateShippingLabel, self).transition_next()

        if self.start.carrier.carrier_cost_method == 'fedex':
            return 'generate'
        return state
