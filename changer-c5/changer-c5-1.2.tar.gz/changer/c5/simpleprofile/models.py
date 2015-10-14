from django.db import models
from django.contrib import admin


class Profile(models.Model):
    """
    User profile model
    """
    user = models.ForeignKey('auth.User', unique=True)
    telephone = models.CharField(max_length=50)

    def __unicode__(self):
        """
        Unicode representation
        """
        return self.user.email


admin.site.register(Profile)
