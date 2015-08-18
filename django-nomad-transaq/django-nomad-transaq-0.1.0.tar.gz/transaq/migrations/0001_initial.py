# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_currency', djmoney.models.fields.CurrencyField(default=b'USD', max_length=3, editable=False, choices=[(b'CLP', 'Chilean peso'), (b'USD', 'US Dollar')])),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=12, blank=True, null=True, verbose_name='amount', default_currency=b'USD')),
                ('creation_dt', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('start_dt', models.DateTimeField(null=True, verbose_name='start date', blank=True)),
                ('end_dt', models.DateTimeField(null=True, verbose_name='end date', blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(1, 'Pending'), (2, 'Done'), (3, 'Verified'), (4, 'Rejected/Canceled/Others')])),
            ],
        ),
    ]
