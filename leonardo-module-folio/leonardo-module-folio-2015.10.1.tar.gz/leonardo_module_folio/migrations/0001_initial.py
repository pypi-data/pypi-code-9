# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import feincms.translations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20150723_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=1, verbose_name='sort order')),
                ('validation', models.CharField(max_length=100, verbose_name='field validations', choices=[(b'webcms.utils.validation.simple', 'One or more characters'), (b'webcms.utils.validation.integer', 'Integer number'), (b'webcms.utils.validation.yesno', 'Yes or No'), (b'webcms.utils.validation.decimal', 'Decimal number')])),
                ('error_message', models.CharField(default='Invalid entry', max_length=100, verbose_name='error message')),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'attribute option',
                'verbose_name_plural': 'attribute options',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='AttributeOptionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('summary', models.CharField(max_length=250, verbose_name='summary', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_folio.AttributeOption')),
            ],
            options={
                'verbose_name': 'attribute option translation',
                'verbose_name_plural': 'attribute option translations',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.SmallIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('mptt_level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('logo', models.ForeignKey(verbose_name='logo', blank=True, to='media.Image', null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='leonardo_module_folio.Category', null=True)),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'portfolio category',
                'verbose_name_plural': 'portfolio categories',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('summary', models.CharField(max_length=250, verbose_name='summary', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_folio.Category')),
            ],
            options={
                'verbose_name': 'category text',
                'verbose_name_plural': 'category texts',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(null=True, verbose_name='ordering', blank=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('logo', models.ForeignKey(verbose_name='logo', blank=True, to='media.Image', null=True)),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='ClientTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('summary', models.CharField(max_length=250, verbose_name='summary', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_folio.Client')),
            ],
            options={
                'verbose_name': 'client translation',
                'verbose_name_plural': 'client translations',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(null=True, blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(to='leonardo_module_folio.Category', verbose_name='categories')),
                ('client', models.ForeignKey(verbose_name='client', blank=True, to='leonardo_module_folio.Client', null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='ProjectAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(blank=True, max_length=10, null=True, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('option', models.ForeignKey(to='leonardo_module_folio.AttributeOption')),
                ('project', models.ForeignKey(to='leonardo_module_folio.Project')),
            ],
            options={
                'ordering': ('option__ordering',),
                'verbose_name': 'Project attribute',
                'verbose_name_plural': 'Project attributes',
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(null=True, verbose_name='ordering', blank=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('featured', models.BooleanField(default=True, verbose_name='featured')),
                ('file', models.ForeignKey(to='media.File')),
                ('project', models.ForeignKey(to='leonardo_module_folio.Project')),
            ],
            options={
                'verbose_name': 'Project file',
                'verbose_name_plural': 'Project files',
            },
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('summary', models.CharField(max_length=250, verbose_name='summary', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_folio.Project')),
            ],
            options={
                'verbose_name': 'project text',
                'verbose_name_plural': 'project texts',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('logo', models.ForeignKey(verbose_name='logo', blank=True, to='media.Image', null=True)),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='ServiceTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('summary', models.CharField(max_length=250, verbose_name='summary', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='leonardo_module_folio.Service')),
            ],
            options={
                'verbose_name': 'service translation',
                'verbose_name_plural': 'service translations',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='files',
            field=models.ManyToManyField(to='media.File', verbose_name='files', through='leonardo_module_folio.ProjectFile', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='media_category',
            field=models.ForeignKey(verbose_name='media category', blank=True, to='media.Folder', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='services',
            field=models.ManyToManyField(to='leonardo_module_folio.Service', verbose_name='services', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('ordering', 'parent')]),
        ),
    ]
