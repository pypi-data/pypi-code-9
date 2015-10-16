# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0002_auto_20150721_0514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=2, serialize=False, verbose_name='Country code', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Country name')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blockrules',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='blacklist.Country', null=True),
            preserve_default=True,
        ),
    ]
