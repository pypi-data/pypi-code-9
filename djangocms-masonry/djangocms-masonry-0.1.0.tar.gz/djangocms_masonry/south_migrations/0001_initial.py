# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Masonry'
        db.create_table(u'djangocms_masonry_masonry', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('extra_options', self.gf('jsonfield.fields.JSONField')(default={}, blank=True)),
            ('column_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=80, null=True, blank=True)),
            ('percent_position', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gutter', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('stamp', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True)),
            ('is_fit_width', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_origin_left', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_origin_top', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('style', self.gf('django.db.models.fields.CharField')(default='default', max_length=255)),
            ('template', self.gf('django.db.models.fields.CharField')(default='default', max_length=255)),
        ))
        db.send_create_signal(u'djangocms_masonry', ['Masonry'])


    def backwards(self, orm):
        # Deleting model 'Masonry'
        db.delete_table(u'djangocms_masonry_masonry')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'djangocms_masonry.masonry': {
            'Meta': {'object_name': 'Masonry'},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'column_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '80', 'null': 'True', 'blank': 'True'}),
            'extra_options': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'gutter': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'is_fit_width': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_origin_left': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_origin_top': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'percent_position': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stamp': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '255'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '255'})
        }
    }

    complete_apps = ['djangocms_masonry']