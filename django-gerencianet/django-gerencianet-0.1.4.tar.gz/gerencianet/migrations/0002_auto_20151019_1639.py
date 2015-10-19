# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gerencianet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentlog',
            options={'verbose_name': 'Log', 'verbose_name_plural': 'Logs'},
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='identifier',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='response',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='status',
            field=models.IntegerField(default=2, choices=[(2, b'Success'), (1, b'Error')]),
        ),
    ]
