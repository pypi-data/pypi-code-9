from django.db import models

from djangocms_text_ckeditor.fields import HTMLField

class Post(models.Model):
    title = models.CharField(verbose_name="Titel", max_length=255)
    pub_date = models.DateTimeField(verbose_name="Gepubliceerd", auto_now_add=True)
    content = HTMLField(verbose_name="Inhoud", blank=True)
    image = models.ImageField(verbose_name="Afbeelding", upload_to="blog", max_length=255, blank=True, null=True)
