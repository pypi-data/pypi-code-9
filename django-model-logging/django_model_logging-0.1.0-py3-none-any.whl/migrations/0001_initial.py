# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pgcrypto.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('operation', models.CharField(max_length=255, choices=[('added', 'Added'), ('removed', 'Removed'), ('modified', 'Modified')])),
                ('model_path', models.CharField(max_length=255)),
                ('data', pgcrypto.fields.TextPGPPublicKeyField(default='')),
                ('creator', models.ForeignKey(null=True, related_name='log_entries_created', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, related_name='log_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
    ]
