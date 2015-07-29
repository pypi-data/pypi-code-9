# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20150723_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menunode',
            name='url',
            field=models.CharField(max_length=512, verbose_name='url', blank=True),
        ),
    ]
