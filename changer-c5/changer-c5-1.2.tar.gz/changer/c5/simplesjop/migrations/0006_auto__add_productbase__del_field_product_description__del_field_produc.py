# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProductBase'
        db.create_table('simplesjop_productbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=200, null=True, blank=True)),
            ('documentation', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('specifications', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['simplesjop.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('simplesjop', ['ProductBase'])

        # Deleting field 'Product.description'
        db.delete_column('simplesjop_product', 'description')

        # Deleting field 'Product.specifications'
        db.delete_column('simplesjop_product', 'specifications')

        # Deleting field 'Product.slug'
        db.delete_column('simplesjop_product', 'slug')

        # Deleting field 'Product.features'
        db.delete_column('simplesjop_product', 'features')

        # Deleting field 'Product.category'
        db.delete_column('simplesjop_product', 'category_id')

        # Deleting field 'Product.name'
        db.delete_column('simplesjop_product', 'name')

        # Deleting field 'Product.documentation'
        db.delete_column('simplesjop_product', 'documentation')

        # Deleting field 'Product.image'
        db.delete_column('simplesjop_product', 'image')

        # Adding field 'Product.base'
        db.add_column('simplesjop_product', 'base', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='versions', to=orm['simplesjop.ProductBase']), keep_default=False)

        # Changing field 'Product.title'
        db.alter_column('simplesjop_product', 'title', self.gf('django.db.models.fields.CharField')(max_length='255'))

        # Changing field 'Category.image'
        db.alter_column('simplesjop_category', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=200, null=True))


    def backwards(self, orm):
        
        # Deleting model 'ProductBase'
        db.delete_table('simplesjop_productbase')

        # Adding field 'Product.description'
        db.add_column('simplesjop_product', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Product.specifications'
        db.add_column('simplesjop_product', 'specifications', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Product.slug'
        db.add_column('simplesjop_product', 'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, db_index=True), keep_default=False)

        # Adding field 'Product.features'
        db.add_column('simplesjop_product', 'features', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Product.category'
        db.add_column('simplesjop_product', 'category', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='products', to=orm['simplesjop.Category']), keep_default=False)

        # Adding field 'Product.name'
        db.add_column('simplesjop_product', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'Product.documentation'
        db.add_column('simplesjop_product', 'documentation', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Product.image'
        db.add_column('simplesjop_product', 'image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True), keep_default=False)

        # Deleting field 'Product.base'
        db.delete_column('simplesjop_product', 'base_id')

        # Changing field 'Product.title'
        db.alter_column('simplesjop_product', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Category.image'
        db.alter_column('simplesjop_category', 'image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'simplesjop.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcategories'", 'null': 'True', 'to': "orm['simplesjop.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'simplesjop.product': {
            'Meta': {'object_name': 'Product'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['simplesjop.ProductBase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'255'"})
        },
        'simplesjop.productbase': {
            'Meta': {'object_name': 'ProductBase'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['simplesjop.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documentation': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'specifications': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'simplesjop.profile': {
            'Meta': {'object_name': 'Profile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['simplesjop']
