# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_auto_20150907_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatcountry',
            name='country',
            field=models.ForeignKey(verbose_name='Country', to='address.Country'),
            preserve_default=True,
        ),
    ]
