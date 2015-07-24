# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rpy2', '0004_resultfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('r_script', models.FileField(upload_to=b'rpy/modules/', verbose_name=b'R Script')),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='availablelibrary',
            options={'verbose_name': 'Library', 'verbose_name_plural': 'Libraries'},
        ),
        migrations.AlterModelOptions(
            name='resultfile',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='scriptresult',
            options={'ordering': ('-started',), 'verbose_name': 'Result', 'verbose_name_plural': 'Results'},
        ),
        migrations.AlterModelOptions(
            name='uploadedscript',
            options={'verbose_name': 'Script', 'verbose_name_plural': 'Scripts'},
        ),
        migrations.AddField(
            model_name='uploadedscript',
            name='modules',
            field=models.ManyToManyField(help_text=b'Optional modules to use in this script.', to='django_rpy2.UploadedModule', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uploadedscript',
            name='libs',
            field=models.ManyToManyField(to='django_rpy2.AvailableLibrary', null=True, verbose_name=b'Libraries', blank=True),
            preserve_default=True,
        ),
    ]
