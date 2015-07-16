# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150621_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='zone',
            field=models.ForeignKey(related_name='clients', to='api.Zone'),
        ),
    ]
