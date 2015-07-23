# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
"""
Moves ScriptResult.fn_out to ScriptResult.files[0] (and back)
"""

def output_file_to_result_files(apps, schema_editor):
    ScriptResult = apps.get_model("django_rpy2", "ScriptResult")
    for result in ScriptResult.objects.all():
        if result.fn_out and result.files.count() == 0:
            result.files.create(fn=result.fn_out)

def result_files_to_output_file(apps, schema_editor):
    ScriptResult = apps.get_model("django_rpy2", "ScriptResult")
    for result in ScriptResult.objects.all():
        if not result.fn_out and result.files.count() > 0:
            result.fn_out = result.files.all()[0].fn
            result.save()

class Migration(migrations.Migration):

    dependencies = [
        ('django_rpy2', '0003_auto_20150401_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fn', models.FileField(upload_to=b'rpy/out/', verbose_name=b'File')),
                ('kind', models.CharField(max_length=12, null=True, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('result', models.ForeignKey(related_name='files', to='django_rpy2.ScriptResult')),
            ],
            options={
                'ordering': ('-order',),
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(output_file_to_result_files, result_files_to_output_file),
        migrations.RemoveField(
            model_name='scriptresult',
            name='fn_out',
        ),
    ]

