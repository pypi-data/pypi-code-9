from django.db import models


class Plugin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=100, blank=True)


class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mac = models.CharField(max_length=100, unique=True, null=True)
    zones = models.ManyToManyField(Zone, related_name='clients')


class Intent(models.Model):
    METHOD_CHOICES = (
        ('POST', 'POST'),
        ('PATCH', 'PATCH'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE')
    )
    name = models.CharField(max_length=100, unique=True)
    method = models.CharField(max_length=6, choices=METHOD_CHOICES)
    api_url = models.CharField(max_length=512)
