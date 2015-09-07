from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Classifier(models.Model):
    name = models.CharField(max_length=255)
    classifier_file = models.FileField(upload_to='classifiers/') #bug in django 1.6
    
class Tag(models.Model):
    name = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name
    
class TestTaggedItem(models.Model):
    id = models.PositiveIntegerField()
    
    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.id)
