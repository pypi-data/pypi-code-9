# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ScraperRunLog.time'
        db.alter_column(u'okscraper_django_scraperrunlog', 'time', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'ScraperRunLog.time'
        db.alter_column(u'okscraper_django_scraperrunlog', 'time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    models = {
        u'okscraper_django.scraperrun': {
            'Meta': {'object_name': 'ScraperRun'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['okscraper_django.ScraperRunLog']", 'symmetrical': 'False'}),
            'scraper_label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'okscraper_django.scraperrunlog': {
            'Meta': {'object_name': 'ScraperRunLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['okscraper_django']