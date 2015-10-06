# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController, config
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import hooks
from tw2.forms import Form, ListLayout, TextField, TextArea, SubmitButton
from tw2.core import StringLengthValidator, Validator
from tgext.pluggable import plug_url, plug_redirect
from tgext.mailer import get_mailer, Message

import logging
log = logging.getLogger('tgapp-contactform')


class SendEmailForm(Form):
    class child(ListLayout):
        subject = TextField(label=None,
                            placeholder=l_('Subject'),
                            validator=StringLengthValidator(min=3, max=64, strip=True, required=True))
        content = TextArea(label=None, validator=Validator(required=True, strip=True, if_empty=''))

    action = plug_url('contactform', '/submit', lazy=True)
    submit = SubmitButton(css_class='btn btn-primary', value=l_('Send'))


class RootController(TGController):
    @expose('contactform.templates.index')
    def index(self, **kwargs):
        return dict(form=SendEmailForm)

    @expose()
    @validate(SendEmailForm, error_handler=index)
    def submit(self, subject='', content=''):
        maildata = {
            'sender': config['_contactform']['sender'],
            'recipients': config['_contactform']['recipients'],
            'subject': subject,
            'body': content,
        }

        maildata = hooks.notify_with_value('contactform.before_send', maildata)

        mailer = get_mailer(request)
        mailer.send_immediately(Message(**maildata))

        flash(_('Your message has been successfully sent'))
        return plug_redirect('contactform', '/')
