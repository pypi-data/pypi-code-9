# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('partner', '0003_auto_20150604_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='VATCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.BooleanField(default=False, verbose_name='Default')),
                ('vat', models.DecimalField(verbose_name='VAT', max_digits=4, decimal_places=2)),
                ('country', models.ForeignKey(verbose_name='Country', to='address.Country', unique=True)),
            ],
            options={
                'verbose_name': 'VAT Country',
                'verbose_name_plural': 'VAT Countries',
            },
            bases=(models.Model,),
        ),
    ]
