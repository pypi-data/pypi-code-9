# -*- coding: utf-8 -*-
from trytond.pool import Pool
from invoice import Invoice, PayInvoiceUsingTransactionStart, \
    PayInvoiceUsingTransaction, PaymentTransaction


def register():
    Pool.register(
        Invoice,
        PaymentTransaction,
        PayInvoiceUsingTransactionStart,
        module='invoice_payment_gateway', type_='model'
    )
    Pool.register(
        PayInvoiceUsingTransaction,
        module='invoice_payment_gateway', type_='wizard'
    )
