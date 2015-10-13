# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('updater', '0001_initial'), ('updater', '0002_notification'), ('updater', '0003_auto_20150923_0854'), ('updater', '0004_auto_20150923_1230'), ('updater', '0005_auto_20151013_1152')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('security_issue', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('registered', models.BooleanField(default=False)),
                ('site_token', models.CharField(default=uuid.uuid4, max_length=36)),
            ],
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Status'},
        ),
    ]
