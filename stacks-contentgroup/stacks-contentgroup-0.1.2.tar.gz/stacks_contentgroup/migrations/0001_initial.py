# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import textplusstuff.fields
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'order',
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name='Order'
                    )
                ),
                (
                    'title',
                    models.CharField(
                        max_length=120,
                        verbose_name='Title'
                    )
                ),
                (
                    'menu_image',
                    versatileimagefield.fields.VersatileImageField(
                        help_text='The menu image for this content.',
                        upload_to=b'content-group/',
                        verbose_name='Menu Image'
                    )
                ),
                (
                    'alternate_menu_image',
                    versatileimagefield.fields.VersatileImageField(
                        help_text="An optional alternate menu image used for "
                                  "'hover' and 'open' states.",
                        upload_to=b'content-group/alternate_image',
                        verbose_name='Alternate Menu Image',
                        blank=True
                    )
                ),
                (
                    'menu_image_ppoi',
                    versatileimagefield.fields.PPOIField(
                        default='0.5x0.5',
                        max_length=20,
                        editable=False
                    )
                ),
                (
                    'alternate_menu_image_ppoi',
                    versatileimagefield.fields.PPOIField(
                        default='0.5x0.5',
                        max_length=20,
                        editable=False
                    )
                ),
                (
                    'content',
                    textplusstuff.fields.TextPlusStuffField(
                        help_text='The content of this section.',
                        null=True,
                        verbose_name='Content',
                        blank=True
                    )
                ),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'name',
                    models.CharField(
                        help_text=(
                            b'The name of this content group. For internal '
                            b'use only.'
                        ),
                        max_length=120,
                        verbose_name='Name'
                    )
                ),
            ],
            options={
                'verbose_name': 'Content Group',
                'verbose_name_plural': 'Content Groups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='content',
            name='group',
            field=models.ForeignKey(
                related_name='content_set',
                verbose_name='Content Group',
                to='stacks_contentgroup.ContentGroup'
            ),
            preserve_default=True,
        ),
    ]
