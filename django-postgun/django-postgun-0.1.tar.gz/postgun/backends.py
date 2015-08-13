import sys
import requests

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


BASE_API_URL = 'https://api.mailgun.net/v3/%s/'


class MailgunAPIError(Exception):
    pass


class MailgunEmailBackend(BaseEmailBackend):
    """
    A simple MailGun Email backend that allows us to send extra goodies
    """

    def __init__(self, fail_silently=False, **kwargs):
        super(MailgunEmailBackend, self).__init__(fail_silently=fail_silently, **kwargs)

        try:
            self.MAILGUN_DOMAIN = getattr(settings, 'MAILGUN_DOMAIN')
            self.MAILGUN_API_KEY = getattr(settings, 'MAILGUN_API_KEY')
        except AttributeError:
            if fail_silently:
                self.MAILGUN_API_KEY, self.MAILGUN_DOMAIN = None, None
            else:
                raise
        self._api_url = BASE_API_URL % self.MAILGUN_DOMAIN
        self.auth = ("api", self.MAILGUN_API_KEY)

    def send_messages(self, email_messages):

        if not email_messages:
            return

        num_sent = 0
        for message in email_messages:
            if self._send_message(message):
                num_sent += 1
        return num_sent

    def _send_message(self, email_message):

        from_email = sanitize_address(email_message.from_email, email_message.encoding)

        recipients = [sanitize_address(addr, email_message.encoding) for addr in email_message.to]

        bcc_recipients = [sanitize_address(addr, email_message.encoding) for addr in email_message.bcc]
        cc_recipients = [sanitize_address(addr, email_message.encoding) for addr in email_message.cc]

        try:
            if sys.version_info > (3, 0):
                text = str(email_message.message().as_string())
            else:
                text = unicode(email_message.message().as_string(), errors="ignore")

            data = {"to": ", ".join(recipients),
                    "subject": email_message.subject,
                    "from": from_email,
                    "text": text
                    }

            if cc_recipients != []:
                data['cc'] = ", ".join(cc_recipients)

            if bcc_recipients != []:
                data['bcc'] = ", ".join(bcc_recipients)

            try:
                mailgun_options = email_message.mailgun_options
                data.update(mailgun_options)
            except AttributeError:
                #We must not be a MailGunMessage
                pass

            files = []
            #Handle alternatives
            for content, mime in email_message.alternatives:
                if 'html' in mime:
                    data.update({'html': content})
                else:
                    #We should probably do something here rather than ignoring it
                    pass
            r = requests.post(self._api_url + "messages",
                              auth=self.auth,
                              data=data,
                              files=files,)
        except requests.ConnectionError:
            if not self.fail_silently:
                raise
            return False

        if r.status_code != 200:
            if not self.fail_silently:
                raise MailgunAPIError(r)
            return False

        return True

    def open(self):
        pass

    def close(self):
        pass
