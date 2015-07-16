# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150622_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('method', models.CharField(max_length=6, choices=[(b'POST', b'POST'), (b'PATCH', b'PATCH'), (b'PUT', b'PUT'), (b'DELETE', b'DELETE')])),
                ('url', models.CharField(max_length=512)),
            ],
        ),
    ]
