# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0004_auto_20150825_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesapayment',
            name='mpesa_code',
            field=models.CharField(help_text='Unique identifier for a payment. This code will be sent to the sender in the receipt.', max_length=128, verbose_name='Code', unique=True),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='mpesa_acc',
            field=models.CharField(help_text='The account entered by the sender on their Pay Bill transaction', max_length=128, verbose_name='Account', blank=True),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='mpesa_amt',
            field=models.DecimalField(verbose_name='Amount', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='original',
            field=jsonfield.fields.JSONField(help_text='A full copy of the original data received from IPN'),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='received',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
