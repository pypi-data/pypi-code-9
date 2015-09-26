from django.db import models
from cms.models import CMSPlugin
from django.utils.encoding import  python_2_unicode_compatible
from embed_video.fields import EmbedVideoField


@python_2_unicode_compatible
class VideoPluginModel(CMSPlugin):
    video_url = EmbedVideoField()
    max_width = models.IntegerField(blank=True, null=True, help_text='in px')

    def __str__(self):
        return self.video_url
