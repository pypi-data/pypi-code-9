from django.db import models
from lisa_api.api.models import Zone


class Controller(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, unique=True)
    port = models.IntegerField(default='50000')
    zone = models.ForeignKey(Zone, null=True)
