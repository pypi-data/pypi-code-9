"""
Relevant constants that should be changed:
- HOSTNAME (localhost for dev)
"""
# redis namespace
PREFIX = "gwsstest"

REDIS_HOSTNAME = "203.117.155.186"

SSDB_HOSTNAME = "localhost"
PORT = 8888

CONFIG = "config"
PATTERN = "pattern"
ACCESS = "access"
ALIAS = "alias" 
URLSET = "urlset"
URLCOUNT = "urlcount"
MACHINEID = "ID"
IPALIAS = "ipalias"
SERVERIP = "serverip"
MESSAGE_QUEUE = "mqueue"

SLEEP = 0.5  # tail sleep frequency
PARSER_UPDATE = 10  # parser check for update

# redis namespace for auto-update component
# not using at the moment
FILTER_JSON = "filter_json"
TIME_JSON = "time_json"