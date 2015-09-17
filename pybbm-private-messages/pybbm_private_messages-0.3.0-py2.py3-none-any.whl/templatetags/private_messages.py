# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

register = template.Library()

@register.assignment_tag
def thread_tail(thread, user, outbox=False):
    if outbox:
        return thread.tail(sender=user)
    return thread.tail(exclude_sender=user)
