# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rq_jobs', '0002_auto_20150721_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='task',
            field=models.CharField(max_length=200, choices=[('djrq.tasks.django_arg_check', 'Django Arg Check'), ('djrq.tasks.django_check', 'Django Check'), ('djrq.more_tasks.more_tasks', 'More Tasks')]),
        ),
    ]
