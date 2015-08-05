#!/bin/env python

import logging
import sys
import os

from scrypture.scrypture import app, load_scripts, load_api, load_config

import argparse

example_config = '''DB_PATH = 'sqlite:///cassava.db'
OPENDNS_APIKEY = ''
VT_API_KEY = ''
PROXIES = {'http_proxy' : None, 'https_proxy' : None}
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cassava')
    parser.add_argument('--initdb', action='store_true',
        help='Initialize the database and local settings files')
    parser.add_argument('--initconfig', action='store_true',
        help='Create a template configuration file')

    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    if args.initdb:
        print "Initializing database."
        from sqlalchemy import create_engine
        db = create_engine('sqlite:///cassava.db')

    if args.initconfig:
        if not os.path.exists('cassava_config.py'):
            f = open('cassava_config.py','w')
            f.write(example_config)
            f.close()
        else:
            print 'Cassava_config.py already exists'

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'NEVERGONNALETYOUDOWN'
    UPLOAD_FOLDER = ''
    SCRIPTS_DIR = 'cassava_scrypture'
    BOOTSTRAP_SERVE_LOCAL = True
    SCRIPT_ROOT = '/'
    LOCAL_DEV = True
    API_BASE_URL = 'http://localhost:5000'
    SCRYPTURE_USERNAME = "Nada"
    SCRYPTURE_PASSWORD = "Nothing"

    try:
        sys.path.insert(0, os.getcwd())
        import cassava_config
        vt_key_present = cassava_config.VT_API_KEY
        opendns_key_present = cassava_config.OPENDNS_APIKEY
        # don't need to actually do anything here, cassava will load this
        # itself
    except ImportError:
        print 'Could not import cassava_config.py'
        print 'Try running run_cassava.py --initconfig'
        vt_key_present = False
        opendns_key_present = False

    virustotal_scripts = ['VirusTotal.virustotal_file',
                          'VirusTotal.virustotal_domain',
                          'VirusTotal.virustotal_ip']

    opendns_scripts = ['OpenDNS.investigate_everything',
                       'OpenDNS.categorization',
                       'OpenDNS.cooccurrences',
                       'OpenDNS.email_whois',
                       'OpenDNS.odns_whois',
                       'OpenDNS.malicious_domains',
                       'OpenDNS.related_domains',
                       'OpenDNS.security_info']

    REGISTERED_SCRIPTS = ['ActiveLookups.whois',
                          'ActiveLookups.dig',
                          'Automater.automater',
                          'Tapioca.tapioca']

    if vt_key_present:
        REGISTERED_SCRIPTS += virustotal_scripts
    if opendns_key_present:
        REGISTERED_SCRIPTS += opendns_scripts

    print 'Starting Cassava in Scrypture at http://localhost:5000'

    app.config['REGISTERED_SCRIPTS'] = REGISTERED_SCRIPTS
    app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SCRIPTS_DIR'] = SCRIPTS_DIR
    app.config['BOOTSTRAP_SERVE_LOCAL'] = BOOTSTRAP_SERVE_LOCAL
    app.config['SCRIPT_ROOT'] = SCRIPT_ROOT
    app.config['LOCAL_DEV'] = LOCAL_DEV
    app.config['API_BASE_URL'] = API_BASE_URL
    app.config['SCRYPTURE_USERNAME'] = SCRYPTURE_USERNAME
    app.config['SCRYPTURE_PASSWORD'] = SCRYPTURE_PASSWORD

    load_scripts()
    app.run(threaded=True, host='0.0.0.0', debug=True)







