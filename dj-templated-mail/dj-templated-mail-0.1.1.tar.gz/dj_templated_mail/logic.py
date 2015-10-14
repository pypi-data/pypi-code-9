# coding: utf-8

import logging

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context, Template

from .models import EmailTemplate


log = logging.getLogger('django_templated_email')


class NoTemplateError(Exception):
    pass


def _render_from_text(text, **context):
    return Template(text).render(Context(context))


def build_templated_mail(
    template_name,
    context,
    recipients,
    sender=None,
    bcc=None,
    cc=None,
    files=None,
):
    html = text = None
    message_cls = EmailMessage
    t = EmailTemplate.objects.filter(template_name__iexact=template_name).first()
    if not t:
        raise NoTemplateError('template "{}" not found'.format(template_name))
    subject = _render_from_text(t.subject, **context)
    text = _render_from_text(t.plain_text, **context)
    if t.html:
        message_cls = EmailMultiAlternatives
        html = _render_from_text(t.html, **context)

    sender = settings.EMAIL_SENDER
    msg = message_cls(subject, text, sender, list(recipients), bcc=bcc, cc=cc)
    if html:
        msg.attach_alternative(html, "text/html")
    files = [] if files is None else files
    for file_data in files:
        msg.attach(*file_data)
    return msg


def send_templated_mail(
    template_name,
    context,
    recipients,
    sender=None,
    bcc=None,
    cc=None,
    files=None,
    fail_silently=False
):
    # remove duplicates from bcc
    if not bcc:
        bcc = []
    if cc:
        bcc = set(bcc) - set(cc)
    bcc = list(set(bcc) - set(recipients))

    log.info('sending mail {} to {}, bcc: {}'.format(template_name, recipients, bcc))
    mail = build_templated_mail(
        template_name,
        context,
        recipients=recipients,
        sender=sender,
        bcc=bcc,
        cc=cc,
        files=files,
    )
    mail.send(fail_silently=fail_silently)
