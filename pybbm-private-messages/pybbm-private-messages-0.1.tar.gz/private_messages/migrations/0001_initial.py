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
            name='MessageHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('body_text', models.TextField(verbose_name='Text version')),
                ('sender_ip', models.IPAddressField(default='0.0.0.0', verbose_name='Sender IP', blank=True)),
                ('sent', models.DateTimeField(auto_now_add=True, verbose_name='Sent', db_index=True)),
                ('subject', models.CharField(default='[No Subject]', max_length=100, blank=True)),
                ('sender_deleted', models.BooleanField(default=False)),
                ('receivers', models.ManyToManyField(related_name='inbox', verbose_name='Recipients', through='private_messages.MessageHandler', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='outbox', verbose_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Private Message',
                'verbose_name_plural': 'Private Messages',
            },
        ),
        migrations.AddField(
            model_name='messagehandler',
            name='message',
            field=models.ForeignKey(to='private_messages.PrivateMessage'),
        ),
        migrations.AddField(
            model_name='messagehandler',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
