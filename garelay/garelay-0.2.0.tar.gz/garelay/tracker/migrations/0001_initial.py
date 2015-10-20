# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=255)),
                ('tracking_id', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('user_agent', models.TextField()),
                ('data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('captured_at', models.DateTimeField(null=True)),
                ('relayed_at', models.DateTimeField(null=True)),
                ('registered_at', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=255, null=True, choices=[(b'captured', b'Captured'), (b'relayed', b'Relayed'), (b'registered', b'Registered')])),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
