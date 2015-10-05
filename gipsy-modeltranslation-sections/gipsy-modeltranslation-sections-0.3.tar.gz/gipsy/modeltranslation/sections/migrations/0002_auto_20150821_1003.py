# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import optionsfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='options',
            field=optionsfield.fields.OptionsField(verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='section',
            name='options_de',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='section',
            name='options_en',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options'),
        ),
        migrations.AlterField(
            model_name='section',
            name='options_fr',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options'),
        ),
    ]
