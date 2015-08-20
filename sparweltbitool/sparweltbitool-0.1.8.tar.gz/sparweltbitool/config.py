import os
import sys
if sys.version_info[:2] >= (3, 4):
    import configparser
    config = configparser.ConfigParser()
else:
    import ConfigParser
    config = ConfigParser.ConfigParser()

config.readfp(open('app/config/config_%s.cfg' % os.environ.get('APP_ENV', 'dev')))
