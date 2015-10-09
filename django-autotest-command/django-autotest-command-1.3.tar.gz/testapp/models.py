
"""
Test models.
"""
from django.db.models import Model, CharField, IntegerField, DateTimeField

class Thing(Model):
    name = CharField(max_length=32)

