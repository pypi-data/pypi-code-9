# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_intent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intent',
            old_name='url',
            new_name='api_url',
        ),
    ]
