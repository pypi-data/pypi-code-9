from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_authentication_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(pre_save, sender=User)
def populate_username(sender, instance=None, **kwargs):
    if not instance.username:
        instance.username = instance.email
