# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lisa_plugins_wifiled', '0002_auto_20150626_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controller',
            name='zone',
            field=models.ForeignKey(to='api.Zone', null=True),
        ),
    ]
