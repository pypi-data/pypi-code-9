# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Condition'
        db.create_table(u'django_condition_chain_condition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'django_condition_chain', ['Condition'])

        # Adding model 'Chain'
        db.create_table(u'django_condition_chain_chain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'django_condition_chain', ['Chain'])

        # Adding model 'ChainElement'
        db.create_table(u'django_condition_chain_chainelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_condition_chain.Chain'])),
            ('joiner', self.gf('django.db.models.fields.CharField')(default=u'and', max_length=3)),
            ('negated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_condition_chain.Condition'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'django_condition_chain', ['ChainElement'])

        # Adding unique constraint on 'ChainElement', fields ['chain', 'order']
        db.create_unique(u'django_condition_chain_chainelement', ['chain_id', 'order'])


    def backwards(self, orm):
        # Removing unique constraint on 'ChainElement', fields ['chain', 'order']
        db.delete_unique(u'django_condition_chain_chainelement', ['chain_id', 'order'])

        # Deleting model 'Condition'
        db.delete_table(u'django_condition_chain_condition')

        # Deleting model 'Chain'
        db.delete_table(u'django_condition_chain_chain')

        # Deleting model 'ChainElement'
        db.delete_table(u'django_condition_chain_chainelement')


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
            'function': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['django_condition_chain']