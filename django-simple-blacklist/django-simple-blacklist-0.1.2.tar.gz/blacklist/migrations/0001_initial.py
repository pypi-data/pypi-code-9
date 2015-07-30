# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='Client IP', protocol='IPv4', blank=True)),
                ('user_agent', models.CharField(help_text='You can specify regexp here', max_length=100, null=True, verbose_name='User Agent', blank=True)),
                ('method', models.CharField(help_text='Empty value means any type of request', max_length=7, null=True, verbose_name='HTTP method', blank=True)),
                ('path', models.CharField(help_text='You can specify regexp here', max_length=200, null=True, verbose_name='Request Path', blank=True)),
                ('view', models.CharField(max_length=100, null=True, verbose_name='Request View', blank=True)),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Block Rule',
                'verbose_name_plural': 'Block Rules',
            },
        ),
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='Client IP', protocol='IPv4')),
                ('user_agent', models.CharField(max_length=100, null=True, verbose_name='User Agent')),
                ('method', models.CharField(max_length=7, verbose_name='HTTP method')),
                ('path', models.SlugField(verbose_name='Request Path', db_index=False)),
                ('view', models.CharField(max_length=100, null=True, verbose_name='Request View')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Request Log',
                'verbose_name_plural': 'Request Logs',
            },
        ),
    ]
