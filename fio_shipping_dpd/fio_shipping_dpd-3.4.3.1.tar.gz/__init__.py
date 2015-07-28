# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from carrier import Carrier, TestConnection, TestConnectionStart
from party import Address
from shipment import ShipmentOut, GenerateShippingLabel, ShippingDPD, Package
from sale import Sale, SaleConfiguration


def register():
    Pool.register(
        Address,
        Carrier,
        SaleConfiguration,
        Sale,
        ShipmentOut,
        ShippingDPD,
        TestConnectionStart,
        Package,
        module='shipping_dpd', type_='model'
    )

    Pool.register(
        TestConnection,
        GenerateShippingLabel,
        module='shipping_dpd', type_='wizard'
    )
