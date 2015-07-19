# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_cascade', '0002_auto_20150530_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='InlineCascadeElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('glossary', jsonfield.fields.JSONField(default={}, blank=True)),
                ('cascade_element', models.ForeignKey(related_name='inline_elements', to='cmsplugin_cascade.CascadeElement')),
            ],
            options={
                'db_table': 'cmsplugin_cascade_inline',
            },
            bases=(models.Model,),
        ),
    ]
