# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_condition_chain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='custom_kwargs',
            field=models.TextField(default='{}', help_text='JSON representation of a dict to pass to the function as extra keyword args.'),
        ),
        migrations.AlterField(
            model_name='chainelement',
            name='joiner',
            field=models.CharField(default='and', max_length=3, choices=[('and', 'and'), ('or', 'or')]),
        ),
    ]
