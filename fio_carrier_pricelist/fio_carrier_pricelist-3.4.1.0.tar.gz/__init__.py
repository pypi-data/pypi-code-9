# -*- coding: utf-8 -*-
from trytond.pool import Pool
from carrier import Carrier
from sale import Sale
from shipment import ShipmentOut


def register():
    Pool.register(
        Sale,
        ShipmentOut,
        Carrier,
        module='carrier_pricelist', type_='model'
    )
