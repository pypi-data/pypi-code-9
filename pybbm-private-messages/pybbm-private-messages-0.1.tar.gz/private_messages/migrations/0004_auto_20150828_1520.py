# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0003_auto_20150828_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='root',
        ),
        migrations.AlterField(
            model_name='privatemessage',
            name='receivers',
            field=models.ManyToManyField(related_name='recd_messages', verbose_name='Recipients', through='private_messages.MessageHandler', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privatemessage',
            name='sender',
            field=models.ForeignKey(related_name='sent_messages', verbose_name='Sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='thread',
            field=models.ForeignKey(related_name='messages', default=1, to='private_messages.MessageThread'),
            preserve_default=False,
        ),
    ]
