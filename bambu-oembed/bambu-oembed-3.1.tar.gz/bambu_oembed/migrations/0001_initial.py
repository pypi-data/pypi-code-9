# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255, db_index=True)),
                ('width', models.PositiveIntegerField()),
                ('html', models.TextField()),
            ],
            options={
                'db_table': 'oembed_resource',
            },
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('url', 'width')]),
        ),
    ]
