# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Email Framework
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import smtplib
import warnings
import logging
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mako.lookup import TemplateLookup

from rattail import exceptions
from rattail.config import parse_list
from rattail.files import resource_path


log = logging.getLogger(__name__)


def deprecation_warning(): # pragma no cover
    warnings.warn(
        "Configuration found in [edbob.mail] section, which is deprecated.  "
        "Please update configuration to use [rattail.mail] instead.",
        DeprecationWarning, stacklevel=2)


def send_message(config, sender, recipients, subject, body, content_type='text/plain'):
    """
    Assemble and deliver an email message using the given parameters and configuration.
    """
    message = make_message(sender, recipients, subject, body, content_type=content_type)
    deliver_message(config, message)


def make_message(sender, recipients, subject, body, content_type='text/plain'):
    """
    Assemble an email message object using the given parameters.
    """
    message = Message()
    message.set_type(content_type)
    message['From'] = sender
    for recipient in recipients:
        message['To'] = recipient
    message['Subject'] = subject
    message.set_payload(body)
    return message
    

def deliver_message(config, message):
    """
    Deliver an email message using the given SMTP configuration.
    """
    server = config.get('rattail.mail', 'smtp.server')
    if not server:
        server = config.get('edbob.mail', 'smtp.server')
        if server:
            deprecation_warning()
        else:
            server = 'localhost'

    username = config.get('rattail.mail', 'smtp.username')
    if not username:
        username = config.get('edbob.mail', 'smtp.username')
        if username:
            deprecation_warning()

    password = config.get('rattail.mail', 'smtp.password')
    if not password:
        password = config.get('edbob.mail', 'smtp.password')
        if password:
            deprecation_warning()

    if config.getboolean('rattail.mail', 'send_emails', default=True):
        log.debug("deliver_message: connecting to server: {0}".format(repr(server)))
        session = smtplib.SMTP(server)
        if username and password:
            result = session.login(username, password)
            log.debug("deliver_message: login result is: {0}".format(repr(result)))
        result = session.sendmail(message['From'], message.get_all('To'), message.as_string())
        log.debug("deliver_message: sendmail result is: {0}".format(repr(result)))
        session.quit()
    else:
        log.debug("config says no emails, but would have sent one to: {0}".format(
            message.get_all('To')))


def send_email(config, key, data={}, subject=None, recipients=None, attachments=None,
               finalize=None, template_key=None):
    """
    Send an email message using configuration, exclusively.

    Assuming a key of ``'foo'``, this should require something like:

    .. code-block:: ini

       [rattail.mail]

       # second line overrides first, just a plain ol' Mako search path
       templates =
           rattail:templates/email
           myproject:templates/email

       foo.subject = [Rattail] Foo Alert
       foo.from = rattail@example.com
       foo.to =
           general-manager@examle.com
           store-manager@example.com
       foo.cc =
           department-heads@example.com
       foo.bcc =
           admin@example.com

    And, the following templates should exist, say in ``rattail``:

    * ``rattail/templates/email/foo.txt.mako``
    * ``rattail/templates/email/foo.html.mako``

    The ``data`` parameter will be passed directly to the template object(s).

    The implementation should look for available template names and react
    accordingly, e.g. if only a plain text is provided then the message will
    not be multi-part at all (unless an attachment(s) requires it).  However if
    both templates are provided then the message will include both parts.

    .. TODO: Flesh out the attachments idea, or perhaps implement finalize only as
    .. it is the most generic?  It would need to be a callback which receives the
    .. actual message object which has been constructed thus far.  It would then
    .. have to return the message object after it had done "other things" to it.

    .. TODO: The attachments idea on the other hand, should allow for a more
    .. declarative (and therefore simpler) approach for the perhaps common case of
    .. just needing to attach a file with a given name and type, etc.  Probably
    .. this should be a simple thing and not require one to specify a callback.
    """
    template = get_template(config, template_key or key)
    body = template.render(**data)
    message = make_message_config(config, key, body, subject=subject,
                                  recipients=recipients,
                                  attachments=attachments)
    deliver_message(config, message)


def get_template(config, key, type_='html'):
    """
    Locate and return the email template corresponding to the provided key.  No
    attempt is made to confirm its existence etc., this just lets the Mako
    logic do its thing.
    """
    templates = parse_list(config.require('rattail.mail', 'templates'))
    templates = [resource_path(p) for p in templates]
    lookup = TemplateLookup(directories=templates)
    return lookup.get_template('{0}.{1}.mako'.format(key, type_))


def make_message_config(config, key, body, subject=None, recipients=None, replyto=None, attachments=None):
    """
    Assemble an email message using configuration, exclusively.

    Assuming a key of ``'foo'``, this should require something like:

    .. code-block:: ini

       [rattail.mail]
       foo.subject = [Rattail] Foo Alert
       foo.from = rattail@example.com
       foo.to =
           general-manager@examle.com
           store-manager@example.com
       foo.cc =
           department-heads@example.com
       foo.bcc =
           admin@example.com
    """
    if attachments is not None:
        message = MIMEMultipart()
        message.attach(MIMEText(body))
        for attachment in attachments:
            message.attach(attachment)
    else:
        message = Message()
        message.set_payload(body, 'utf_8')
        message.set_type('text/html')

    message['From'] = get_sender(config, key)
    if replyto is None:
        replyto = get_replyto(config, key)
    if replyto:
        message.add_header('Reply-To', replyto)
    if recipients is None:
        recipients = get_recipients(config, key)
    for recipient in recipients:
        message['To'] = recipient
    if subject is None:
        subject = get_subject(config, key)
    message['Subject'] = subject
    return message


def get_sender(config, key):
    """
    Get the sender (From:) address for an email message.
    """
    sender = config.get('rattail.mail', '{0}.from'.format(key))
    if sender:
        return sender
    sender = config.get('rattail.mail', 'default.from')
    if sender:
        return sender

    # Allow legacy settings, for now.
    sender = config.get('edbob.mail', 'sender.{0}'.format(key))
    if sender:
        deprecation_warning()
        return sender
    sender = config.get('edbob.mail', 'sender.default')
    if sender:
        deprecation_warning()
        return sender

    raise exceptions.SenderNotFound(key)


def get_replyto(config, key):
    """
    Get the Reply-To address for an email message.
    """
    replyto = config.get('rattail.mail', '{0}.replyto'.format(key))
    if replyto:
        return replyto
    replyto = config.get('rattail.mail', 'default.replyto')
    if replyto:
        return replyto


def get_recipients(config, key):
    """
    Get the list of recipients (To:) addresses for an email message.
    """
    recipients = config.get('rattail.mail', '{0}.to'.format(key))
    if recipients:
        return parse_list(recipients)
    recipients = config.get('rattail.mail', 'default.to')
    if recipients:
        return parse_list(recipients)

    # Allow legacy settings, for now.
    recipients = config.get('edbob.mail', 'recipients.{0}'.format(key))
    if recipients:
        return eval(recipients)
    recipients = config.get('edbob.mail', 'recipients.default')
    if recipients:
        return eval(recipients)

    raise exceptions.RecipientsNotFound(key)


def get_subject(config, key):
    """
    Get the subject for an email message.
    """
    subject = config.get('rattail.mail', '{0}.subject'.format(key))
    if subject:
        return subject
    subject = config.get('rattail.mail', 'default.subject')
    if subject:
        return subject

    # Allow legacy settings, for now.
    subject = config.get('edbob.mail', 'subject.{0}'.format(key))
    if subject:
        return subject
    subject = config.get('edbob.mail', 'subject.default')
    if subject:
        return subject

    # Fall back to a sane default.
    return "[Rattail] Automated Message"
