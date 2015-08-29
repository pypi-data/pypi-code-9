# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0002_auto_20150826_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessage',
            name='id',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
    ]
