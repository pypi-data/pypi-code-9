import os
import pymysql


pymysql.install_as_MySQLdb()


def eval_file(filename):
    try:
        f = open(filename).read()
        return eval(f)
    except IOError:
        return {}


def is_private_ip(ip):
    return ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('127.')


def get_mysql_conf(key):
    return eval_file('/etc/jiemo/mysql.py').get(key, None)


def get_mysql_conf_db(db):
    conf = get_mysql_conf(db)
    if conf:
        conf['db'] = db
    return conf


def get_mysql_django_conf(key):
    conf = get_mysql_conf(key)
    return conf if not conf else {'HOST': conf['host'], 'USER': conf['user'], 'PASSWORD': conf['passwd']}


def get_local_settings(file):
    return eval_file(os.path.join(os.path.dirname(os.path.abspath(file)), 'local_settings.py'))


