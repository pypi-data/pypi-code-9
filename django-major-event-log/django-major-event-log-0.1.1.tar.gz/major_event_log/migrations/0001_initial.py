# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('detail', models.TextField()),
                ('outcome', models.CharField(max_length=255)),
                ('outcome_detail', models.TextField()),
                ('date', models.DateTimeField()),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
                ('entry_modified', models.DateTimeField(auto_now=True)),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
