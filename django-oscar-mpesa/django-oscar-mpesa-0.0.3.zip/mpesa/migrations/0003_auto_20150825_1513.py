# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


FIELD_MAPPING = {
    "ipn_id": "id",
    "origin": "orig",
    "destination": "dest",
    "recieved_at": "tstamp",
    "message": "text",
    "reference_number": "mpesa_code",
    "subscriber_phone_number": "mpesa_msisdn",
    "subscriber_name": "mpesa_sender",
    "amount": "mpesa_amt",
    "account": "mpesa_acc",
    "paybill_number": "business_number",
    "customer_id": "customer_id",
}
TRANSACTION_DATE_FORMAT = "%d/%m/%y"
TRANSACTION_TIME_FORMAT = "%I:%M %p"
TSTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def remap_fields(apps, schema_editor):
    MpesaPayment = apps.get_model("mpesa", "MpesaPayment")
    for payment in MpesaPayment.objects.all():
        # Copy values for amount and account
        payment.mpesa_acc = payment.account
        payment.mpesa_amt = payment.amount
        payment.mpesa_code = payment.reference_number
        # Use recieved_at to provide values for received
        payment.received = payment.recieved_at
        # Map all the old fields to the 'original' json field
        json = {new: getattr(payment, old)
                for old, new in FIELD_MAPPING.items()}
        # Split transaction_datetime
        json['mpesa_trx_date'] = payment.transaction_datetime.strftime(TRANSACTION_DATE_FORMAT)
        json['mpesa_trx_time'] = payment.transaction_datetime.strftime(TRANSACTION_TIME_FORMAT)
        # Format 'recieved_at'
        json['tstamp'] = payment.recieved_at.strftime(TSTAMP_FORMAT)
        payment.original = json
        payment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_auto_20150825_1513'),
    ]

    operations = [
        migrations.RunPython(remap_fields),
    ]
