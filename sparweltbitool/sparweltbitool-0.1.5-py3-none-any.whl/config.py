import configparser
import os

config = configparser.ConfigParser()
config.readfp(open('app/config/config_%s.cfg' % os.environ.get('APP_ENV', 'dev')))
