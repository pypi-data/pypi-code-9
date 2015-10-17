# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='additional',
            field=models.TextField(default='N/A'),
        ),
    ]
