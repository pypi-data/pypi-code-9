from django.db import models

# Create your models here.
class Classifier(models.Model):
    name = models.CharField(max_length=255)
    classifier_file = models.FileField(upload_to='') #bug in django 1.6
    
