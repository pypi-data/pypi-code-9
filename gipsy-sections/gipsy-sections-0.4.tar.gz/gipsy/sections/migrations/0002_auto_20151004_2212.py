# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import optionsfield.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='section',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='section',
            name='options',
            field=optionsfield.fields.OptionsField(verbose_name='options', types=(basestring,)),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_object_id',
            field=models.PositiveIntegerField(help_text="Specifies object to which this section is attached to. Do not change if you're unsure what does that it do.", null=True, blank=True),
        ),
    ]
