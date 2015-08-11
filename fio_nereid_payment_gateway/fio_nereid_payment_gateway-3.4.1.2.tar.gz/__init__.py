# -*- coding: utf-8 -*-
from trytond.pool import Pool
from party import Party, PaymentProfile
from website import Website


def register():
    Pool.register(
        Party,
        PaymentProfile,
        Website,
        module='nereid_payment_gateway', type_='model'
    )
