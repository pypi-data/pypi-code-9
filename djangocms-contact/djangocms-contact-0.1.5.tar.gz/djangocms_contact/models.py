from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class ContactMessage(models.Model):
    """A model to store the contact messages data."""

    name = models.CharField(max_length=64, verbose_name=_('Name'))
    email = models.EmailField(max_length=254, verbose_name=_('Email'))
    subject = models.CharField(max_length=255, blank=True,
                               verbose_name=_('Subject'))
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name=_('Creation date'))
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')

    def __str__(self):
        return self.subject
