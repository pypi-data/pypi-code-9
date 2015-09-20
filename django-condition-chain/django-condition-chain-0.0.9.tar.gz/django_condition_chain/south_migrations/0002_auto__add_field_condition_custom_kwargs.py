# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Condition.custom_kwargs'
        db.add_column(u'django_condition_chain_condition', 'custom_kwargs',
                      self.gf('django.db.models.fields.TextField')(default=u'{}'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Condition.custom_kwargs'
        db.delete_column(u'django_condition_chain_condition', 'custom_kwargs')


    models = {
        u'django_condition_chain.chain': {
            'Meta': {'object_name': 'Chain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'django_condition_chain.chainelement': {
            'Meta': {'unique_together': "((u'chain', u'order'),)", 'object_name': 'ChainElement'},
            'chain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_condition_chain.Chain']"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_condition_chain.Condition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joiner': ('django.db.models.fields.CharField', [], {'default': "u'and'", 'max_length': '3'}),
            'negated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'django_condition_chain.condition': {
            'Meta': {'object_name': 'Condition'},
            'custom_kwargs': ('django.db.models.fields.TextField', [], {'default': "u'{}'"}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['django_condition_chain']