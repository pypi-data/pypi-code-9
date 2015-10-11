#!/usr/bin/env python
# -*- coding:utf-8 -*


import logging
from logging.handlers import RotatingFileHandler
import sys, os, re
import traceback as tb

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

str_levels = {DEBUG: "DEBUG", INFO : "INFO",WARNING : "WARNING",ERROR : "ERROR",CRITICAL : "CRITICAL"}

#TODO : ajouter un email_level ... et accepter unicode.
#TODO : améliorer les argv (cas multiple, logfile, ...




class my_logging():
	'''Une classe pour gérer mes loggings
		A instancier une fois par programme.
		Permet à partir du Rootlogger de
			générer 
				une sortie console
				une sortie fichier
				
		Usage :
			from my_logging import *
			
			my_logging(DEBUG,'toto.log', WARNING)
			logging.debug("hello")
			or
			log = my_logging(DEBUG,'toto.log', WARNING)
			log.debug("hello")
	'''
	def __init__(self, console_level = None, name_logfile = None, logfile_level = None, email_level = None, log_name = None, max_file_size = 10000000, max_file_nb = 5, details = False):
		'''Création des handler pour console et fichier
			- console_level		:	DEBUG, INFO, WARNING, ERROR, CRITICAL
			- name_logfile		:	name of the file to log
			- logfile_level		:	DEBUG, INFO, WARNING, ERROR, CRITICAL
			- email_level		:	DEBUG, INFO, WARNING, ERROR, CRITICAL
			- log_name			:	name of the logger
			- max_file_size		:	maximum size for the log file (default is 10 Mo)
			- max_file_nb		:	maximum number of log files (default is 5)
			- details			:	if True, pathname and lineno are added
		'''
		self.max_file_size = max_file_size
		self.max_file_nb = max_file_nb
		self.details = details
		# Initialisation des niveaux None => 0 (pour faire les min(...)
		if console_level == None:
			console_level = 0
		if logfile_level == None:
			logfile_level = 0
		if email_level == None:
			email_level = 0
		#Initialisation des handlers à None
		self.file_handler = None
		self.console_handler = None
		self.mail_handler = None
		#Initialisation des niveaux
		#Si aucun niveau n'est spécifié, on regarde dans le sys.argv
		if not (console_level or logfile_level or email_level):
			if self.level_in_argv():
				if name_logfile:
					logfile_level = self.level_in_argv()
				else:
					console_level = self.level_in_argv()
			# Si rien dans sys.argv, on prend DEBUG par defaut
			else:
				if name_logfile:
					logfile_level = console_level = DEBUG
				else:
					console_level = DEBUG
		# Initilialisation du logger
		if log_name:
			self.logger = logging.getLogger(log_name)
		else:
			self.logger = logging.getLogger()
		self.logger.setLevel(min(console_level,logfile_level, email_level))
		# Initialisation du mode Console
		if console_level:
			self.add_console_handler(console_level)
		# Initlialisation du mode fichier
		if name_logfile:
			if logfile_level == None:
				logfile_level = console_level
			self.add_file_handler(name_logfile, logfile_level)
		else:
			if logfile_level:
				# Par defaut le fichier de log est a le même nom que le programme + 'log'
				# et ce trouve dans le repertoire du script
				name_logfile = os.path.splitext(sys.argv[0])[0] + '.log'
				self.add_file_handler(name_logfile, logfile_level)
		if email_level:
			self.add_email_handler(email_level)
		#Pour loggin des execptions
		sys.excepthook = self.log_exception_hook
		logging.info("my_logging logger is started. Console : %s. File (%s) : %s" % (str_levels[console_level], name_logfile, str_levels[logfile_level]))
		
	# def __del__(self):
		# '''Destructor'''
		# if self.logger:
			# if self.file_handler:
				# self.logger.removeHandler(self.file_handler)
			# if self.console_handler:
				# self.logger.removeHandler(self.console_handler)
			# if self.mail_handler:
				# self.logger.removeHandler(self.mail_handler)
		
	def add_file_handler(self, name_logfile, logfile_level):
		'''Add a file handler to logger
			- name_logfile		:	name of the file to log
			- logfile_level		:	DEBUG, INFO, WARNING, ERROR, CRITICAL	
		'''
		if self.details:
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s at %(pathname)s ,line n°:%(lineno)s')
		else:
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		self.file_handler = RotatingFileHandler(name_logfile, 'a', self.max_file_size, self.max_file_nb)
		self.file_handler.setLevel(logfile_level)
		self.file_handler.setFormatter(formatter)
		self.logger.addHandler(self.file_handler)
	
	def add_console_handler(self, console_level):
		'''Add a console handler to logger
			- console_level		:	DEBUG, INFO, WARNING, ERROR, CRITICAL
		'''
		self.console_handler = logging.StreamHandler()
		self.console_handler.setLevel(console_level)
		self.logger.addHandler(self.console_handler)
		
	def add_email_handler(self, email_level):
		'''Add a email handler
		'''
		#TODO...
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		self.mail_handler = SMTPHandler( \
			# Host et port
			('SMTP.GMAIL.COM', 587), \
			# From
			"MOI@GMAIL.COM", \
			# To (liste)
			["QUELQU.UN@QUELQUE.PART"], \
			# Sujet du message
			"Erreur critique dans %s" % nom_loggeur, \
			# pour l'authentification
			credentials = ("MONEMAIL@GMAIL.COM", "MONSUPERPASSWORD"), \
			secure = ())
		self.mail_handler.setLevel(email_level)
		szelf.mail_handler.setFormatter(formatter)
		self.logger.addHandler(self.mail_handler)
		
	def debug(self, text=None, *args, **kwargs):
		'''log text in DEBUG level'''
		self.logger.log(logging.DEBUG, text, *args, **kwargs)
	def info(self, text=None, *args, **kwargs):
		'''log text in INFO level'''
		self.logger.log(logging.INFO, text, *args, **kwargs)
	def warning(self, text=None, *args, **kwargs):
		'''log text in WARNING level'''
		self.logger.log(logging.WARNING, text, *args, **kwargs)
	def error(self, text=None, *args, **kwargs):
		'''log text in ERROR level'''
		self.logger.log(logging.ERROR, text, *args, **kwargs)
	def critical(self, text=None, *args, **kwargs):
		'''log text in CRITICAL level'''
		self.logger.log(logging.CRITICAL, text, *args, **kwargs)		
	def level_in_argv(self):
		if len(sys.argv)>1:
			for level, str_level in str_levels.items():
				if re.match("^([-]{0,2}(%s))$" % str_level, sys.argv[1].upper()):
					return level
	
	def log_exception_hook(self, type, value, traceback):
		'''Log les exceptions
		'''
		self.logger.error(''.join(tb.format_tb(traceback)))
		self.logger.error('{0} - {1}'.format(type, value))