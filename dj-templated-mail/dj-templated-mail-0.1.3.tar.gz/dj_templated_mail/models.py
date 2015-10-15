# coding: utf-8

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class EmailTemplate(models.Model):

    """
    Since these are more likely to be changed than other templates, we store
    them in the database.

    This means that an admin can change email templates without having to have
    access to the filesystem.
    """

    template_name = models.CharField(max_length=100)

    subject = models.TextField()

    plain_text = models.TextField(null=True, blank=True)

    html = models.TextField(null=True, blank=True)

    def __str__(self):
        return '<EmailTemplate: {}>'.format(self.template_name)
