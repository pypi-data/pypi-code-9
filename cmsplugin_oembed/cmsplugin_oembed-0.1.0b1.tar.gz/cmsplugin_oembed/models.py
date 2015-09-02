from django.db import models
from cms.models import CMSPlugin
from django.utils.encoding import  python_2_unicode_compatible
from embed_video.fields import EmbedVideoField


@python_2_unicode_compatible
class VideoPluginModel(CMSPlugin):
    name = models.CharField(
        blank=True,
        max_length=50
    )
    video_url = EmbedVideoField()

    def __str__(self):
        return self.name
