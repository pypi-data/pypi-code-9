# -*- coding: utf-8 -*-
"""
================================================================================
    Zentrale Konfigurationsdatei ITYOU ESI
 
================================================================================
"""
import logging
from App.config import getConfiguration


# --- ESI-Version --------------
ESI_VERSION = "ITYOU ESI - 1.3rc2"

# --- buildout configurations --------------------------------------------------
config = getConfiguration()
pc = config.product_config.get('ityou_esi', dict())

# --- postgres connection uri --------------------------------------------------
PSQL_DB =       pc.get('psql_db')           
PSQL_USERNAME = pc.get('psql_username')     
PSQL_PASSWORD = pc.get('psql_password')     
PSQL_HOST =     pc.get('psql_host')         
PSQL_PORT =     pc.get('psql_port')

PSQL_URI = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (PSQL_USERNAME, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DB)
psql_uri_log = 'postgresql+psycopg2://%s:XXXXXXXX@%s:%s/%s' % (PSQL_USERNAME, PSQL_HOST, PSQL_PORT, PSQL_DB)

logging.info('----> Postgresql connection string: %s' % psql_uri_log)

# --- postgres installation ----------------------
#   create database ityou_esi;
#   create user ityou_esi_user with password 'XXXXXXX';
#   grant all on database ityou_esi to ityou_esi_user;


# --- REDIS Server ------------------
REDIS_SERVER    = pc.get('redis_server') or '127.0.0.1'
REDIS_KEY       = pc.get('redis_key') or PSQL_DB

logging.info('----> Redis connection: %s / %s' %(REDIS_SERVER, REDIS_KEY))

ZOPE_INSTANCE = INSTANCE_HOME.split('/')[-4].replace('-','_').replace('.', '_')
ESI_FLAGS_KEY   = ZOPE_INSTANCE + '_' + "esi:ajaxflags_" + REDIS_KEY




