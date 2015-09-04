# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'mpesa', '0001_initial'), (b'mpesa', '0002_auto_20141013_1222'), (b'mpesa', '0003_auto_20141015_1142'), (b'mpesa', '0004_auto_20141021_1539'), (b'mpesa', '0005_auto_20150824_1603')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipn_id', models.CharField(unique=True, max_length=256, verbose_name='The IPN id.')),
                ('origin', models.CharField(max_length=128, verbose_name='This is the source of the notification.')),
                ('destination', models.CharField(max_length=128, verbose_name='Your business terminal MSISDN (phone number)')),
                ('recieved_at', models.DateTimeField(verbose_name='The date and time at which the IPN was received')),
                ('message', models.TextField(verbose_name='The text message received from M-Pesa')),
                ('reference_number', models.CharField(unique=True, max_length=16)),
                ('account', models.CharField(max_length=128, null=True, verbose_name='The account entered by the subscriber on their Pay Bill transaction', blank=True)),
                ('subscriber_phone_number', models.CharField(max_length=128, verbose_name='The phone number from which this payment was made.')),
                ('subscriber_name', models.CharField(max_length=128, verbose_name="The sender's name")),
                ('transaction_datetime', models.DateTimeField(blank=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('paybill_number', models.IntegerField(verbose_name='The Pay Bill number used for this transaction')),
                ('customer_id', models.CharField(max_length=128)),
            ],
        ),
    ]
