# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_auto_20150727_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='menunode',
            name='url_de',
            field=models.CharField(max_length=512, null=True, verbose_name='url', blank=True),
        ),
        migrations.AddField(
            model_name='menunode',
            name='url_en',
            field=models.CharField(max_length=512, null=True, verbose_name='url', blank=True),
        ),
        migrations.AddField(
            model_name='menunode',
            name='url_fr',
            field=models.CharField(max_length=512, null=True, verbose_name='url', blank=True),
        ),
    ]
