from django.db import models


class LiveSetting(models.Model):
    LIVESETTING_TYPES = (
        ('bool', 'bool'),
        ('str', 'str'),
        ('int', 'int'),
        ('float', 'float'),
        ('json', 'json'),
        ('yaml', 'yaml'),
        ('schematics', 'schematics'),
    )

    key = models.CharField(max_length=128, primary_key=True)
    key_type = models.CharField(max_length=256, choices=LIVESETTING_TYPES)
    value = models.TextField()
