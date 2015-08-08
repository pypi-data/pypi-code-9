import os
import uuid

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .conf import UPLOAD_TO, USER_MODEL


def picture_upload_to(instance, filename):
    """
    Returns a unique filename for picture which is hard to guess.
    Will use uuid.uuid4() the chances of collision are very very very low.
    """
    ext = os.path.splitext(filename)[1].strip('.')
    if not ext:
        ext = 'jpg'
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join(UPLOAD_TO, filename)


class Picture(models.Model):
    image = models.ImageField(upload_to=picture_upload_to)
    user = models.ForeignKey(USER_MODEL, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)


@receiver(post_delete, sender=Picture, dispatch_uid="croppic_picture_delete_signal")
def picture_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    instance.image.delete(save=False)
