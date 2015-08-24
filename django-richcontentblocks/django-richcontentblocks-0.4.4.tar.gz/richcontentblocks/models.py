from django.db import models
from django.db.models.signals import post_save, post_delete
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.core.cache import cache


class Content(models.Model):
    CONTENT_BLOCK = 'CB'
    PAGE = 'PG'
    BLOCK_TYPE_CHOICES = (
        (CONTENT_BLOCK, 'Content Block'),
        (PAGE, 'Page')
    )

    title = models.CharField(max_length=50, blank=False)
    key = models.SlugField(unique=True, blank=True,
                            help_text="The key used to access the content block in a template.  The system will generate this for you.")
    content = RichTextField(blank=False)
    content_group = models.CharField(max_length=50, blank=True, null=False,
                                    help_text="Logical group this item belongs to.  Leave blank if none.")
    content_type = models.CharField(max_length=2,
                                      choices=BLOCK_TYPE_CHOICES,
                                      default=CONTENT_BLOCK)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Content Block'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.key = slugify(self.title)
        super(Content, self).save(*args, **kwargs)

    @staticmethod
    def get_content_by_key(key):
        obj = cache.get(key)

        if obj is None:
            try:
                obj = Content.objects.get(key=key)
                cache.set(key, obj)
            except Content.DoesNotExist:
                obj = None

        return obj


def clear_content_from_cache(sender, instance, **kwargs):
    """
    :description - clears content block from cache if it exists
    """
    obj = cache.get(instance.key)
    if obj:
        cache.delete(instance.key)

# register the signal
post_save.connect(clear_content_from_cache, sender=Content, dispatch_uid="save_clear_content_from_cache")
post_delete.connect(clear_content_from_cache, sender=Content, dispatch_uid="delete_clear_content_from_cache")