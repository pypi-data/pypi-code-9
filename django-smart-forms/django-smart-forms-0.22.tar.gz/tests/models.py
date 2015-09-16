from django.db import models


class Example(models.Model):
    a = models.CharField(max_length=3)
    b = models.IntegerField()


class Example2(models.Model):
    c = models.CharField(max_length=2)
    d = models.IntegerField(blank=True, null=True)