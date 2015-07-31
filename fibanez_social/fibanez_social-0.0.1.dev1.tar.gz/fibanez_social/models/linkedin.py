
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Linkedin(models.Model):
    website_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.website_url
    
    class Meta:
        """
        Linkedin's meta informations.
        """
        app_label = 'fibanez_social'
    