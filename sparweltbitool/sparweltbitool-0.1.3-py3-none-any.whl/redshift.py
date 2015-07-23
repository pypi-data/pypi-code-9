import psycopg2

from sparweltbitool.config import config
from sparweltbitool.singleton import Singleton

@Singleton
class RedshiftSingleton(object):
    """ Operations with Redshift database."""

    def __init__(self):
        parameters = {
            'host': config.get('database', 'host'),
            'dbname': config.get('database', 'dbname'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password'),
            'port': config.get('database', 'port')
        }
        self.conn = psycopg2.connect("host='%(host)s' dbname='%(dbname)s' user='%(user)s' password='%(password)s' port='%(port)s'" % parameters)
        self.conn.autocommit = True

    def __del__(self):
        self.conn.close()
