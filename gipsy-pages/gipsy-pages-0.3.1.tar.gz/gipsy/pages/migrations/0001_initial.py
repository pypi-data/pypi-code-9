# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
import django.utils.timezone
from django.conf import settings
import optionsfield.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(0, 'Inactive'), (1, 'Active')])),
                ('activate_date', models.DateTimeField(help_text='keep empty for an immediate activation', null=True, blank=True)),
                ('deactivate_date', models.DateTimeField(help_text='keep empty for indefinite activation', null=True, blank=True)),
                ('created_by', models.CharField(verbose_name='Created by', max_length=128, null=True, editable=False, blank=True)),
                ('modified_by', models.CharField(verbose_name='Modified by', max_length=128, null=True, editable=False, blank=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('section_ptr', models.PositiveIntegerField()),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Image', blank=True)),
                ('template_name', models.CharField(max_length=255, null=True, verbose_name='template', blank=True)),
                ('options', optionsfield.fields.OptionsField(verbose_name='options', types=(unicode, str))),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('slug', models.SlugField(verbose_name='slug', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('author', models.ForeignKey(verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='pages.Page', null=True)),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
