# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.translations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('web_address', models.CharField(max_length=255, verbose_name='Link')),
                ('target', models.CharField(default=b'_none', max_length=255, verbose_name='target', choices=[(b'_none', 'Same window'), (b'_blank', 'New window'), (b'_modal', 'Modal window')])),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('ordering', models.PositiveIntegerField(default=0, verbose_name='Ordering')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'Link item',
                'verbose_name_plural': 'Link items',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='LinkCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.CharField(max_length=255, verbose_name='slug', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'Link list',
                'verbose_name_plural': 'Link lists',
            },
        ),
        migrations.CreateModel(
            name='LinkTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_links.Link')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.ForeignKey(verbose_name='List', to='leonardo_module_links.LinkCategory'),
        ),
        migrations.AddField(
            model_name='link',
            name='image',
            field=models.ForeignKey(verbose_name='Image', blank=True, to='media.Image', null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='relationship',
            field=models.ForeignKey(verbose_name='link relationship', blank=True, to='leonardo_module_links.Link', null=True),
        ),
    ]
