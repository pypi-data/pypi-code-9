# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import cms.models.fields
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('filer', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallToAction',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'db_table': 'calltoaction_plugins',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CallToActionRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('style', models.CharField(default=b'calltoaction/default.html', max_length=200, choices=[(b'calltoaction/default.html', b'default')])),
                ('image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True)),
                ('link_to_page', cms.models.fields.PageField(blank=True, to='cms.Page', null=True)),
            ],
            options={
                'db_table': 'calltoaction_repository',
                'verbose_name': 'Call to Action Repository',
                'verbose_name_plural': 'Call to Action',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallToActionRepositoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('content', djangocms_text_ckeditor.fields.HTMLField(blank=True)),
                ('link_text', models.CharField(max_length=100, blank=True)),
                ('link_custom', models.CharField(max_length=400, blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='calltoaction.CallToActionRepository', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'calltoaction_repository_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'Call to Action Repository Translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='calltoactionrepositorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='calltoaction',
            name='call_to_action',
            field=models.ForeignKey(to='calltoaction.CallToActionRepository'),
            preserve_default=True,
        ),
    ]
