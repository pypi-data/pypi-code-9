# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150622_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='zone',
        ),
        migrations.AddField(
            model_name='client',
            name='zones',
            field=models.ManyToManyField(related_name='clients', to='api.Zone'),
        ),
    ]
