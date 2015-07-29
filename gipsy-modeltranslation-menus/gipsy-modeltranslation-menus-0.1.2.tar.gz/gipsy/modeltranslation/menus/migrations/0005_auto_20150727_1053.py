# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import optionsfield.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_auto_20150723_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='menunode',
            name='description_de',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='menunode',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='menunode',
            name='description_fr',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='menunode',
            name='options_de',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options', types=(unicode, str)),
        ),
        migrations.AddField(
            model_name='menunode',
            name='options_en',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options', types=(unicode, str)),
        ),
        migrations.AddField(
            model_name='menunode',
            name='options_fr',
            field=optionsfield.fields.OptionsField(null=True, verbose_name='options', types=(unicode, str)),
        ),
        migrations.AddField(
            model_name='menunode',
            name='slug_de',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'title', editable=False, blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='menunode',
            name='slug_en',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'title', editable=False, blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='menunode',
            name='slug_fr',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'title', editable=False, blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='menunode',
            name='title_de',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='menunode',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='menunode',
            name='title_fr',
            field=models.CharField(max_length=255, null=True, verbose_name='title'),
        ),
    ]
