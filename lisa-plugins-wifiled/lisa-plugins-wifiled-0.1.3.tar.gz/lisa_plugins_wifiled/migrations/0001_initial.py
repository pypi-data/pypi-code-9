# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150622_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('address', models.CharField(unique=True, max_length=100)),
                ('port', models.CharField(max_length=5)),
                ('user', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('zone', models.ForeignKey(to='api.Zone', blank=True)),
            ],
        ),
    ]
