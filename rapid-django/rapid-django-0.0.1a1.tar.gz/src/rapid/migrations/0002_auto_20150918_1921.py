# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
import rapid


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(rapid, ['initial_data.json'])),

    ]
