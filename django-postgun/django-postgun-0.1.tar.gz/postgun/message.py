from django.core.mail.message import EmailMultiAlternatives, sanitize_address


class MailGunMessage(EmailMultiAlternatives):

    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None, tags=None, campaign=None, delivery_time=None,
                 dkim=None, track=None, track_clicks=None, track_opens=None, custom_headers=None, reply_to=None):
        self.tags = tags
        self.campaign = campaign
        self.delivery_time = delivery_time
        self.dkim = dkim
        self.track = track
        self.track_clicks = track_clicks
        self.track_opens = track_opens
        self.custom_headers = custom_headers
        self.reply_to = reply_to
        super(MailGunMessage, self).__init__(subject=subject, body=body, from_email=from_email, to=to, bcc=bcc,
                                             connection=connection, attachments=attachments, headers=headers, cc=cc,
                                             reply_to=self.reply_to)

    @property
    def mailgun_options(self):
        options = {}

        if self.tags is not None: options['o:tag'] = self.tags
        if self.campaign is not None: options['o:campaign'] = self.campaign
        if self.delivery_time is not None: options['o:deliverytime'] = self.delivery_time
        if self.dkim is not None: options['o:dkim'] = self.dkim
        if self.track is not None: options['o:tracking'] = self.track
        if self.track_clicks is not None: options['o:tracking-clicks'] = self.track_clicks
        if self.track_opens is not None: options['o:tracking-opens'] = self.track_opens
        if self.reply_to is not None: options['h:Reply-To'] = [sanitize_address(reply_to, self.encoding) for reply_to in self.reply_to]
        if self.custom_headers is not None:
            try:
                for key, value in list(self.custom_headers.items()):
                    header = 'h:%s' % key
                    options[header] = value
            except AttributeError:
                pass
        return options
