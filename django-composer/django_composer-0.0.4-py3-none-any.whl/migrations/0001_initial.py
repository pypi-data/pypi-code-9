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
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('is_dynamic', models.BooleanField(default=False)),
                ('last_changed', models.DateTimeField(auto_now=True)),
                ('has_changed', models.BooleanField(default=False)),
                ('context_example', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('changed_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='element',
            unique_together=set([('name', 'template_name')]),
        ),
        migrations.AlterIndexTogether(
            name='element',
            index_together=set([('name', 'template_name')]),
        ),
    ]
