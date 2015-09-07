# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_vatcountry'),
    ]

    operations = [
        migrations.CreateModel(
            name='VATType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('default', models.BooleanField(default=False, verbose_name='Default')),
            ],
            options={
                'verbose_name': 'VAT Type',
                'verbose_name_plural': 'VAT Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vatcountry',
            name='vat_type',
            field=models.ForeignKey(default=1, verbose_name='VAT Type', to='partner.VATType'),
            preserve_default=False,
        ),
    ]
