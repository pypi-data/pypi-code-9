import os
import pymysql

# 有些用了pymysql的地方import本模块之后可以省去下面这一行的调用
pymysql.install_as_MySQLdb()


# 主要用于读取文件中的配置
def eval_file(filename):
    try:
        f = open(filename).read()
        return eval(f)
    except IOError:
        return {}


# 判断是否是私网ip，172开头的网段有待后续实现
def is_private_ip(ip):
    return ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('127.')


# 获取mysql的配置
def get_mysql_conf(key):
    return eval_file('/etc/jiemo/mysql.py').get(key, None)


# 获取mysql配置，加上db参数
def get_mysql_conf_db(db):
    conf = get_mysql_conf(db)
    if conf:
        conf['db'] = db
    return conf


# 将普通mysql的配置转成django的配置
def get_mysql_django_conf(key):
    conf = get_mysql_conf(key)
    return conf if not conf else {'HOST': conf['host'], 'USER': conf['user'], 'PASSWORD': conf['passwd']}


# 获取本地配置，生产环境有些配置与测试不同，不同的配置可以放在local_settings.py
def get_local_settings(file):
    return eval_file(os.path.join(os.path.dirname(os.path.abspath(file)), 'local_settings.py'))


