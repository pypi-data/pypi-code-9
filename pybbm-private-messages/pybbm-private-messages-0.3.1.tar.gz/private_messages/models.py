# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

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


class MessageThread(models.Model):

    class Meta:
        ordering = ('-messages',)

    @property
    def head(self):
        return self.messages.earliest()

    def tail(self, exclude_sender=None, sender=None):
        assert exclude_sender is None or sender is None, "Cannot set both kwargs exclude_sender and sender"
        qs = self.messages.all()
        if exclude_sender is not None:
            qs = qs.exclude(sender=exclude_sender)
        elif sender is not None:
            qs = qs.filter(sender=sender)
        return qs.latest()

    def get_parents(self, message):
        assert self.messages.filter(message=message).exists(), "Cannot get parents of a message not in this thread"
        return self.messages.filter(sent__lt=message.sent)


@python_2_unicode_compatible
class PrivateMessage(RenderableItem):

    class Meta(object):
        verbose_name = _('Private Message')
        verbose_name_plural = _('Private Messages')
        get_latest_by = 'sent'
        ordering = ['sent']

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(get_user_model_path(),
                               related_name='sent_messages',
                               verbose_name=_('Sender'))
    sender_ip = models.IPAddressField(_('Sender IP'),
                                      blank=True,
                                      default='0.0.0.0')
    sent = models.DateTimeField(_('Sent'), auto_now_add=True, db_index=True)
    subject = models.CharField(max_length=100, blank=True, default='[No Subject]')
    receivers = models.ManyToManyField(get_user_model_path(),
                                       through='MessageHandler',
                                       related_name='recd_messages',
                                       verbose_name=_('Recipients'))
    # Expected behaviour when deleting a sent message is that the recipient still has their copy
    sender_deleted = models.BooleanField(default=False)
    thread = models.ForeignKey(MessageThread, related_name='messages')

    def __str__(self):
        return '{0} {1}'.format(_('Private message from'), self.sender)

    def get_absolute_url(self):
        return reverse('private_messages:read_message', kwargs={'pk': self.uuid})

    def save(self, *args, **kwargs):
        self.render()
        super(PrivateMessage, self).save(*args, **kwargs)

    def get_children(self):
        return self.thread.messages.filter(sent__gt=self.sent)

    def get_parent(self):
        try:
            parent = self.thread.messages.filter(sent__lt=self.sent).latest()
        except PrivateMessage.DoesNotExist:
            return None
        return parent

    def unread(self, user):
        try:
            handler = MessageHandler.objects.get(message=self, receiver=user)
        except MessageHandler.DoesNotExist:
            return False
        return not handler.read

    def get_parents(self):
        """
        This method is just a hack for adding the Inbox to the breadcrumbs in read_message view. To get all the parents
        of a message, use message.thread.get_parents(message)
        """
        return [_InboxLink()]


class _InboxLink(object):
    __slots__ = ()

    @staticmethod
    def get_absolute_url():
        return reverse('private_messages:inbox')

    def __repr__(self):
        return _('Inbox')
