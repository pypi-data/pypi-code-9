# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import optionsfield.fields
import filebrowser.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(0, 'Inactive'), (1, 'Active')])),
                ('activate_date', models.DateTimeField(help_text='keep empty for an immediate activation', null=True, blank=True)),
                ('deactivate_date', models.DateTimeField(help_text='keep empty for indefinite activation', null=True, blank=True)),
                ('created_by', models.CharField(verbose_name='Created by', max_length=128, null=True, editable=False, blank=True)),
                ('modified_by', models.CharField(verbose_name='Modified by', max_length=128, null=True, editable=False, blank=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Image', blank=True)),
                ('template_name', models.CharField(max_length=255, null=True, verbose_name='template', blank=True)),
                ('options', optionsfield.fields.OptionsField(verbose_name='options', types=(unicode, str))),
                ('section_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('section_content_type', models.ForeignKey(related_name='sections', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('order',),
                'get_latest_by': 'created',
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
        ),
    ]
