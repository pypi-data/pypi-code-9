# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(unique=True, max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(default=b'', max_length=255, blank=True)),
                ('expires', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'get_latest_by': 'id',
                'verbose_name': 'user hash',
                'verbose_name_plural': 'user hashes',
            },
        ),
    ]
