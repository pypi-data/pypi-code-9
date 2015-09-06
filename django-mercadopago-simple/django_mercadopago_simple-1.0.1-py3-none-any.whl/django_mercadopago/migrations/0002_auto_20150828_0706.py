# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('topic', models.CharField(choices=[('o', 'Merchant Order'), ('p', 'Payment')], max_length=1)),
                ('resource_id', models.CharField(max_length=46)),
                ('processed', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='approved',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 7, 6, 10, 663643)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='mp_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('topic', 'resource_id')]),
        ),
    ]
