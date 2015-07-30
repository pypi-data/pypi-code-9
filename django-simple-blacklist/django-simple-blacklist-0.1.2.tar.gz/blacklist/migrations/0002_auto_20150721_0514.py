# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockrules',
            name='user_agent',
            field=models.CharField(help_text='You can specify regexp here', max_length=256, null=True, verbose_name='User Agent', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='user_agent',
            field=models.CharField(max_length=256, null=True, verbose_name='User Agent'),
            preserve_default=True,
        ),
    ]
