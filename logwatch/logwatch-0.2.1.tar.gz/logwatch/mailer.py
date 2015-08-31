#!/usr/bin/python
import os
import smtplib
from yamlcfg import YamlConfig

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer(object):

    def __init__(self, from_email=None, to_email=None, subject_prefix=None,
            username=None, password=None, mail_server=None, mail_port=None,
            **kwargs):
        self.from_email = from_email
        self.to_email = to_email
        self.subject_prefix = subject_prefix or ''
        self.username = username
        self.password = password
        self.mail_server = mail_server
        self.mail_port = mail_port

    def send_email(self, subject, body, from_email=None, to_email=None):
        from_email = from_email or self.from_email
        to_email = to_email or self.to_email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject_prefix + subject
        msg['From'] = from_email
        msg['To'] = to_email
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)
        s = smtplib.SMTP(self.mail_server, self.mail_port)
        s.starttls()
        s.login(self.username, self.password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()
