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
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=255)),
                ('response', models.IntegerField()),
                ('ip', models.GenericIPAddressField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('additional', models.CharField(default=b'N/A', max_length=255)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
