# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lisa_plugins_wifiled', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controller',
            name='password',
        ),
        migrations.RemoveField(
            model_name='controller',
            name='user',
        ),
        migrations.AlterField(
            model_name='controller',
            name='port',
            field=models.IntegerField(default=b'50000'),
        ),
    ]
