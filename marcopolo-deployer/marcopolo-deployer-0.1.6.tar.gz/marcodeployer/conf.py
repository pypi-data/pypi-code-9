# -*- coding: utf-8 -*-
from os.path import dirname, join, isabs
import tempfile
import logging
import six
from six.moves import configparser

CONF_DIR = '/etc/marcodeployer'

CERTS = "/usr/lib/marcodeployer/certs"
APPCERT = "app.crt"
APPKEY = "app.key"
RECEIVERCERT = "receiver.crt"
RECEIVERKEY = "receiver.key"

TMPDIR = join(tempfile.gettempdir(), "tmp_deployer")

STATIC_PATH = "/usr/lib/marcodeployer/static"
TOMCAT_PATH = '/var/lib/tomcat7/webapps/'

DEPLOYER_PORT = 1342
RECEIVER_PORT = 1339
RECEIVER_WEBSOCKET_PORT = 1370
NON_SECURE_DEPLOYER_PORT = 1442

INTERFACE = 'eth0'

REFRESH_FREQ = 1000.0

STATUS_MONITOR_SERVICE_NAME = "statusmonitor"
DEPLOYER_SERVICE_NAME = "deployer"
RECEIVER_SERVICE_NAME = "receiver"

TEMPLATES_DIR = "/usr/lib/marcodeployer/templates/"

LOGGING_DIR = "/var/log/marcopolo"
DEPLOYER_LOG_FILE = "/var/log/marcodeployer/marcodeployerd.log"
RECEIVER_LOG_FILE = "/var/log/marcodeployer/marcoreceiverd.log"

DEPLOYER_LOGLEVEL = "DEBUG"
RECEIVER_LOGLEVEL = "DEBUG"

SECRET_FILE = "/etc/marcodeployer/secret"


default_values = {
    "CERTS": CERTS,
    "APPCERT": APPCERT if isabs(APPCERT) else join(CERTS, APPCERT),
    "APPKEY": APPKEY if isabs(APPKEY) else join(CERTS, APPKEY),
    "RECEIVERCERT": RECEIVERCERT if isabs(RECEIVERCERT) else join(CERTS, RECEIVERCERT),
    "RECEIVERKEY": RECEIVERKEY if isabs(RECEIVERKEY) else join(CERTS, RECEIVERKEY),
    "TMPDIR" : TMPDIR if isabs(TMPDIR) else join(tempfile.gettempdir(), TMPDIR),
    "STATIC_PATH": STATIC_PATH,
    "TOMCAT_PATH": TOMCAT_PATH,
    "DEPLOYER_PORT" : DEPLOYER_PORT,
    "RECEIVER_PORT" : RECEIVER_PORT,
    "RECEIVER_WEBSOCKET_PORT" : RECEIVER_WEBSOCKET_PORT,
    "INTERFACE":INTERFACE,
    "REFRESH_FREQ": REFRESH_FREQ,
    "STATUS_MONITOR_SERVICE_NAME" : STATUS_MONITOR_SERVICE_NAME,
    "DEPLOYER_SERVICE_NAME" : DEPLOYER_SERVICE_NAME,
    "RECEIVER_SERVICE_NAME" : RECEIVER_SERVICE_NAME,
    "TEMPLATES_DIR" : TEMPLATES_DIR,
    "LOGGING_DIR" : LOGGING_DIR,
    "DEPLOYER_LOG_FILE" : DEPLOYER_LOG_FILE,
    "RECEIVER_LOG_FILE" : RECEIVER_LOG_FILE,
    "DEPLOYER_LOGLEVEL" : DEPLOYER_LOGLEVEL,
    "RECEIVER_LOGLEVEL" : RECEIVER_LOGLEVEL,
    "SECRET_FILE": SECRET_FILE,
    "NON_SECURE_DEPLOYER_PORT" : NON_SECURE_DEPLOYER_PORT,
}

config = configparser.RawConfigParser(default_values, allow_no_value=False)

DEPLOYER_FILE_READ = join(CONF_DIR, 'deployer.cfg')


try:
    with open(DEPLOYER_FILE_READ, 'r') as df:
        config.readfp(df)

        CERTS = config.get('common', 'CERTS')
        
        APPCERT = config.get('deployer', 'APPCERT')
        APPCERT = APPCERT if isabs(APPCERT) else join(CERTS, APPCERT)

        APPKEY = config.get('deployer', 'APPKEY')
        APPKEY = APPKEY if isabs(APPKEY) else join(CERTS, APPKEY)

        RECEIVERCERT = config.get('receiver', 'RECEIVERCERT')
        RECEIVERCERT = RECEIVERCERT if isabs(RECEIVERCERT) else join(CERTS, RECEIVERCERT)
        
        RECEIVERKEY = config.get('receiver', 'RECEIVERKEY')
        RECEIVERKEY = RECEIVERKEY if isabs(RECEIVERKEY) else join(CERTS, RECEIVERKEY)

        TMPDIR = config.get('deployer', 'TMPDIR')
        
        STATIC_PATH = config.get('deployer', 'STATIC_PATH')
        TOMCAT_PATH = config.get('deployer', 'TOMCAT_PATH')
        DEPLOYER_PORT = config.getint('deployer', 'DEPLOYER_PORT')
        RECEIVER_PORT = config.getint('receiver', 'RECEIVER_PORT')
        RECEIVER_WEBSOCKET_PORT = config.getint('receiver', 'RECEIVER_WEBSOCKET_PORT')
        INTERFACE = config.get('receiver', 'INTERFACE')
        REFRESH_FREQ = config.getfloat('receiver', 'REFRESH_FREQ')
        STATUS_MONITOR_SERVICE_NAME = config.get('receiver', 'STATUS_MONITOR_SERVICE_NAME')
        DEPLOYER_SERVICE_NAME = config.get('deployer', 'DEPLOYER_SERVICE_NAME')
        RECEIVER_SERVICE_NAME = config.get('receiver', 'RECEIVER_SERVICE_NAME')
        TEMPLATES_DIR = config.get('deployer', 'TEMPLATES_DIR')
        LOGGING_DIR = config.get('common', 'LOGGING_DIR')
        DEPLOYER_LOG_FILE = config.get('deployer', 'DEPLOYER_LOG_FILE')
        RECEIVER_LOG_FILE = config.get('receiver', 'RECEIVER_LOG_FILE')
        DEPLOYER_LOGLEVEL = config.get('deployer', 'DEPLOYER_LOGLEVEL')
        RECEIVER_LOGLEVEL = config.get('receiver', 'RECEIVER_LOGLEVEL')
        SECRET_FILE = config.get('receiver', 'SECRET_FILE')
        NON_SECURE_DEPLOYER_PORT = config.get('deployer', 'NON_SECURE_DEPLOYER_PORT')

except IOError as i:
    logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
except Exception as e:
    logging.warning("Unknown exception in configuration parser %s" % e)