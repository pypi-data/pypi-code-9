#!/usr/bin/env python
# -*- coding:utf-8 -*

from email.mime.text import MIMEText
import logging
import smtplib

class gmail:
	'''SMTP gmail
	'''
	def __init__(self, gmail_account, gmail_pwd):
		self.gmail_account = gmail_account
		self.gmail_pwd = gmail_pwd
		
	def send_mail(self, to_email, subject, message):
		logging.info('Sending email : to:%s subject:%s message:%s'%(to_email, subject, message))
		message = format(message)
		message = MIMEText(message, _charset = "utf-8")
		message.add_header("Subject", subject)
		message.add_header("From", self.gmail_account)
		message.add_header("To", to_email)
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.ehlo()
			server.starttls()
			server.login(self.gmail_account, self.gmail_pwd)
			server.sendmail(self.gmail_account, to_email, message.as_string())
			server.close()
			return True
		except Exception , e:
			logging.error('Erreur sending email :' + str(e))
			return False