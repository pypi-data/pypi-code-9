# coding=utf-8
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

__author__ = 'franki'


class UserHash(models.Model):
    """
    Hash system for Django. Features:
    - Hashes are associated to users.
    - A hash is created for a specific use.
    - You associate an optional value to the hash.
    - Hash expire
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    hash = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True, default='')
    expires = models.DateTimeField()

    class Meta:
        ordering = ['id']
        get_latest_by = 'id'
        verbose_name = _("user hash")
        verbose_name_plural = _("user hashes")

    @classmethod
    def create(cls, user, key, value='', duration_seconds=24 * 3600):
        """
        Creates a hash instance. In some cases, like in a confirmation for an order, you may have the same key
        with different values. Ex: order_confirmation=order-12, order_confirmation=order-32.
        :param user: Django user to associate the hash to
        :param key: Key for the hash. (confirmation_email, order_confirmation)
        :param value: String. Optional.
        :param duration_minutes: Defaults to 24 hours
        :return: Created UserHash instance.
        """
        expires = timezone.now() + timezone.timedelta(seconds=duration_seconds)
        hash = str(uuid.uuid4())

        userhash = UserHash()
        userhash.user = user
        userhash.expires = expires
        userhash.hash = hash
        userhash.key = key
        userhash.value = value
        userhash.save()
        return hash

    @classmethod
    def fetch(cls, hash, key):
        """
        For a given hash and key returns the user and the value.
        :param hash:
        :param key:
        :return: (user, value)
        """
        userhash = UserHash.objects.get(
            expires__gte=timezone.now(),
            hash=hash,
            key=key
        )
        return userhash.user, userhash.value

    @classmethod
    def clear(cls, hash):
        """
        Deletes a given hash
        :param hash:
        """
        userhash = UserHash.objects.get(hash=hash)
        userhash.delete()

    @classmethod
    def fetch_and_clear(cls, hash, key):
        """
        For a given hash and key returns the user and the value and deletes the hash.
        :param hash:
        :param key:
        :return: (user, value)
        """
        userhash = UserHash.objects.get(
            expires__gte=timezone.now(),
            hash=hash,
            key=key
        )
        userhash.delete()
        return userhash.user, userhash.value

    @classmethod
    def for_user(cls, user, key):
        """
        Returns a list of al hashes a user has for a given key. Useful to cleanup or check for existence.
        :param user:
        :param key:
        :return: QuerySet
        """
        hashes = UserHash.objects.filter(
            expires__gte=timezone.now(),
            user=user,
            key=key
        )
        return hashes

