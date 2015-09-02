#!/bin/python

import ConfigParser
import os
import logging
import imaplib
import time
import signal

from boxup_types import Colorcodes
from boxup_types import MatrixData

# Load from config file
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("boxup_gmailunread")
logger.info("Reading config-file...")

config = ConfigParser.ConfigParser()
config.read('/etc/boxup/plugins/boxup_gmailunread.cfg')

MAX_DATA_AGE = config.getint('Settings','MAX_DATA_AGE')
USERNAME = config.get('Settings','USERNAME')
PASSWORD = config.get('Settings','PASSWORD')
TRESHHOLD_ORANGE = config.getint('Settings','TRESHHOLD_ORANGE')
TRESHHOLD_RED = config.getint('Settings','TRESHHOLD_RED')


class GmailunreadMatrixData (MatrixData):
	def __init__(self):
		self._unread = 0
		self._lastUpdate = 0
	def setWidth(self):
		logger.warning("GmailunreadMatrixData is currently only supporting 8x8")
		pass
	def setHeight(self):
		logger.warning("GmailunreadMatrixData is currently only supporting 8x8")
		pass
	def getPx(self,x,y):
		unread = self._getUnread()
		logger.info("x: "+str(x)+" y: "+str(y))
		logger.info("Unread mails: "+str(unread))
		fieldnum = ((8*y)+x+1)
		if unread >= fieldnum:
			if fieldnum > TRESHHOLD_RED:
				return Colorcodes.RED
			elif fieldnum > TRESHHOLD_ORANGE:
				return Colorcodes.ORANGE
			else:
				return Colorcodes.GREEN
		else:
			return Colorcodes.OFF
	def _getUnread(self):
		logger.info(self._lastUpdate - time.time())
		if time.time() - self._lastUpdate <= MAX_DATA_AGE:
			return self._unread
		try:
			logger.info("make imap call")
			obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
			obj.login(USERNAME,PASSWORD)
			obj.select()
			self._lastUpdate = time.time()
			self._unread = len(obj.search(None, 'UnSeen')[1][0].split())
			return self._unread
		except:
			pass
		

if __name__ == "__main__":
	logger.info("dont run as __main__. its a boxup module")
else:
	logger.info("boxup_gmailunread is running as module")

