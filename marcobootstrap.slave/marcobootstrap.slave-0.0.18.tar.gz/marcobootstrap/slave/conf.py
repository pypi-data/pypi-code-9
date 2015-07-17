# -*- coding: utf-8 -*-
from os.path import dirname, join, isabs
import logging
import six, sys
from six.moves import configparser

CONF_DIR = "/etc/marcobootstrap/slave/"

cert_dir = "/etc/marcobootstrap/slave/certs"

certs = cert_dir

APPCERT = join(certs, "app.crt")
APPKEY  = join(certs, "app.key")

RECEIVERCERT = join(certs, "receiver.crt")
RECEIVERKEY = join(certs, "receiver.key")

ADMIN = "admin"
ADMIN_PASS = '$5$rounds=110000$H6PevFw6VZ.IiUqL$beL6q6C9R6dVqFUQLtWsHYzXyOqoqBYOa13Z1lR5Z.1'

LOG_FILENAME = "/var/log/marcopolo/marco-bootstrap-slave.log"
LOG_LEVEL = "DEBUG"

BOOTDIR = '/boot/'
BOOTPARTITION = '/dev/mmcblk0'
BOOTCODE_FALLBACK = '/etc/marcobootstrap/code.zip'
TMP_DIR = '/tmp'
REBOOT_MSG = "Reinicio del sistema en 2 minutos"
DEBUG = True

SERVICE_NAME = "marco-bootstrap-slave"
BACKEND_FILES_PORT = 1345
SLAVE_PORT = 1360

default_values = {
    'cert_dir':cert_dir,
    'certs':certs,
    'APPCERT':APPCERT,
    'APPKEY ':APPKEY ,
    'RECEIVERCERT':RECEIVERCERT,
    'RECEIVERKEY':RECEIVERKEY,
    'ADMIN':ADMIN,
    'ADMIN_PASS':ADMIN_PASS,
    'LOG_FILENAME':LOG_FILENAME,
    'LOG_LEVEL':LOG_LEVEL,
    'BOOTDIR':BOOTDIR,
    'BOOTPARTITION':BOOTPARTITION,
    'BOOTCODE_FALLBACK':BOOTCODE_FALLBACK,
    'TMP_DIR':TMP_DIR,
    'REBOOT_MSG':REBOOT_MSG,
    'DEBUG':DEBUG,
    'SERVICE_NAME':SERVICE_NAME,
    'BACKEND_FILES_PORT':BACKEND_FILES_PORT,
    'SLAVE_PORT':SLAVE_PORT
}

config = configparser.RawConfigParser(default_values, allow_no_value=False)

SLAVE_FILE_READ = join(CONF_DIR, 'slave.cfg')

try:
    with open(SLAVE_FILE_READ, 'r') as df:
        config.readfp(df)
        
        cert_dir = config.get('slave', 'cert_dir')
        certs = config.get('slave', 'certs')
        
        APPCERT = config.get('slave', 'APPCERT')
        APPCERT = APPCERT if isabs(APPCERT) else join(certs, APPCERT)

        APPKEY = config.get('slave', 'APPKEY')
        APPKEY = APPKEY if isabs(APPKEY) else join(certs, APPKEY)

        RECEIVERCERT = config.get('slave', 'RECEIVERCERT')
        RECEIVERCERT = RECEIVERCERT if isabs(RECEIVERCERT) else join(certs, RECEIVERCERT)

        RECEIVERKEY = config.get('slave', 'RECEIVERKEY')
        RECEIVERKEY = RECEIVERKEY if isabs(RECEIVERKEY) else join(certs, RECEIVERKEY)

        STATIC_PATH = config.get('slave', 'STATIC_PATH')
        ADMIN = config.get('slave', 'ADMIN')
        ADMIN_PASS = config.get('slave', 'ADMIN_PASS')
        LOG_FILENAME = config.get('slave', 'LOG_FILENAME')
        LOG_LEVEL = config.get('slave', 'LOG_LEVEL')
        BOOTDIR = config.get('slave', 'BOOTDIR')
        BOOTPARTITION = config.get('slave', 'BOOTPARTITION')
        BOOTCODE_FALLBACK = config.get('slave', 'BOOTCODE_FALLBACK')
        TMP_DIR = config.get('slave', 'TMP_DIR')
        REBOOT_MSG = config.get('slave', 'REBOOT_MSG')
        DEBUG = config.getboolean('slave', 'DEBUG')
        SERVICE_NAME = config.get('slave', 'SERVICE_NAME')
        BACKEND_FILES_PORT = config.getint('slave', 'BACKEND_FILES_PORT')
        SLAVE_PORT = config.getint('slave', 'SLAVE_PORT')

except IOError as i:
    logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
except Exception as e:
    logging.warning("Unknown exception in configuration parser: %s" % e)
