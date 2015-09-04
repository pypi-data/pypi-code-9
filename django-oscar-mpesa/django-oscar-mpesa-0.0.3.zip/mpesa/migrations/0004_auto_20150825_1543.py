# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0003_auto_20150825_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mpesapayment',
            name='account',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='ipn_id',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='message',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='paybill_number',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='recieved_at',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='reference_number',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='subscriber_name',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='subscriber_phone_number',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='transaction_datetime',
        ),
    ]
