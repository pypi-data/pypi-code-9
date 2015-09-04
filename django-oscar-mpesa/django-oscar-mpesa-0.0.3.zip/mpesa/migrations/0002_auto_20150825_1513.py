# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_squashed_0005_auto_20150824_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpesapayment',
            name='mpesa_code',
            field=models.CharField(help_text='Unique identifier for a payment. This code will be sent to the sender in the receipt.', max_length=128, null=True, verbose_name='Code', unique=True),
        ),
        migrations.AddField(
            model_name='mpesapayment',
            name='mpesa_acc',
            field=models.CharField(help_text='The account entered by the subscriber on their Pay Bill transaction', max_length=128, null=True, verbose_name='Account'),
        ),
        migrations.AddField(
            model_name='mpesapayment',
            name='mpesa_amt',
            field=models.DecimalField(null=True, verbose_name='Amount', max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='mpesapayment',
            name='original',
            field=jsonfield.fields.JSONField(help_text='A full copy of the original data received from IPN', null=True),
        ),
        migrations.AddField(
            model_name='mpesapayment',
            name='received',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
