# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0004_auto_20141021_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesapayment',
            name='account',
            field=models.CharField(max_length=128, null=True, verbose_name='The account entered by the subscriber on their Pay Bill transaction', blank=True),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='destination',
            field=models.CharField(max_length=128, verbose_name='Your business terminal MSISDN (phone number)'),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='paybill_number',
            field=models.IntegerField(verbose_name='The Pay Bill number used for this transaction'),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='subscriber_phone_number',
            field=models.CharField(max_length=128, verbose_name='The phone number from which this payment was made.'),
        ),
    ]
