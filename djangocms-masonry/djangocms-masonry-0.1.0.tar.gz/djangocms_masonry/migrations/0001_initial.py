# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Masonry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('extra_options', jsonfield.fields.JSONField(default={}, verbose_name='JSON options', blank=True)),
                ('column_width', models.PositiveSmallIntegerField(default=80, help_text='Aligns items to a horizontal grid.', null=True, blank=True)),
                ('percent_position', models.BooleanField(default=False, help_text='Sets item positions in percent values, rather than pixel values.percentPosition: true works well with percent-width items, as items will not transition their position on resize.')),
                ('gutter', models.PositiveSmallIntegerField(default=0, help_text='Adds horizontal space between item elements.')),
                ('stamp', models.CharField(default='', help_text='Specifies which elements are stamped within the layout.Isotope will layout items below stamped elements.', max_length=128, blank=True)),
                ('is_fit_width', models.BooleanField(default=False, help_text="Sets the width of the container to fit the available number of columns, based the size of container's parent element. When enabled, you can center the container with CSS.")),
                ('is_origin_left', models.BooleanField(default=True, help_text='Controls the horizontal flow of the layout. By default, item elements start positioning at the left, with isOriginLeft: true. Set isOriginLeft: false for right-to-left layouts.')),
                ('is_origin_top', models.BooleanField(default=True, help_text='Controls the vertical flow of the layout. By default, item elements start positioning at the top, with isOriginTop: true. Set isOriginTop: false for bottom-up layouts. It\u2019s like Tetris!')),
                ('style', models.CharField(default=b'default', help_text='CSS class', max_length=255, verbose_name='style', choices=[(b'default', 'Default')])),
                ('template', models.CharField(default=b'default', max_length=255, verbose_name='template', choices=[(b'default', 'Default')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
