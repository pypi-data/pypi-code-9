# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'ordering': ['sent'], 'get_latest_by': 'sent', 'verbose_name': 'Private Message', 'verbose_name_plural': 'Private Messages'},
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='parent',
            field=models.ForeignKey(related_name='child', to='private_messages.PrivateMessage', null=True),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='root',
            field=models.ForeignKey(to='private_messages.PrivateMessage', null=True),
        ),
    ]
