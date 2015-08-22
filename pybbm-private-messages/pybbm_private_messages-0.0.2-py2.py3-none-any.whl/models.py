# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from pybb.compat import get_user_model_path
from pybb.models import RenderableItem


class MessageHandler(models.Model):

    message = models.ForeignKey('PrivateMessage')
    receiver = models.ForeignKey(get_user_model_path())
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


@python_2_unicode_compatible
class PrivateMessage(RenderableItem):

    class Meta(object):
        verbose_name = _('Private Message')
        verbose_name_plural = _('Private Messages')

    sender = models.ForeignKey(get_user_model_path(),
                               related_name='outbox',
                               verbose_name=_('Sender'))
    sender_ip = models.IPAddressField(_('Sender IP'),
                                      blank=True,
                                      default='0.0.0.0')
    sent = models.DateTimeField(_('Sent'), auto_now_add=True, db_index=True)
    subject = models.CharField(max_length=100, blank=True, default='[No Subject]')
    receivers = models.ManyToManyField(get_user_model_path(),
                                       through='MessageHandler',
                                       related_name='inbox',
                                       verbose_name=_('Recipients'))
    # Expected behaviour when deleting a sent message is that the recipient still has their copy
    sender_deleted = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([str(self.sender), _('Private Message'), str(self.id)])

    def get_absolute_url(self):
        return reverse('pybb:private_message', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
      self.render()
      super(PrivateMessage, self).save(*args, **kwargs)
