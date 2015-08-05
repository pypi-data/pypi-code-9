import sys
import os

OPENDNS_APIKEY = ''
VT_API_KEY = ''
ISIGHT_PUBKEY = ''
ISIGHT_PRIVKEY = ''

DB_PATH = ''
PROXIES = {}

try: # try importing cassava_config from the working directory
    sys.path.insert(0, os.getcwd())
    import cassava_config
    if hasattr(cassava_config, 'ISIGHT_PUBKEY'):
        ISIGHT_PUBKEY = cassava_config.ISIGHT_PUBKEY
    if hasattr(cassava_config, 'ISIGHT_PRIVKEY'):
        ISIGHT_PRIVKEY = cassava_config.ISIGHT_PRIVKEY
    if hasattr(cassava_config, 'VT_API_KEY'):
        VT_API_KEY = cassava_config.VT_API_KEY
    if hasattr(cassava_config, 'OPENDNS_APIKEY'):
        OPENDNS_APIKEY = cassava_config.OPENDNS_APIKEY
    if hasattr(cassava_config, 'DB_PATH'):
        DB_PATH = cassava_config.DB_PATH
    if hasattr(cassava_config, 'PROXIES'):
        PROXIES = cassava_config.PROXIES
except ImportError:
    print 'No API keys defined!'
    print 'Create a cassava_config.py or set manually (e.g., cassava.config.VT_API_KEY = "YOURKEY")'

