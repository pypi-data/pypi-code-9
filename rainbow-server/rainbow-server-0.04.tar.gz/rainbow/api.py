
import time
import random
from hashlib import sha1
import ConfigParser
from optparse import OptionParser
import logging as log
import traceback

from config import g_CONFIG
import settings
log.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)


def get_parser():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="config_filename", type="string")
    parser.add_option("-p", "--port", dest="port", type="string")

    return parser


def init_config():
    parser = get_parser()
    options, args = parser.parse_args()
    if not getattr(options, 'config_filename', None):
        log.error('miss -f')
        return False

    try:
        config = ConfigParser.SafeConfigParser()
        config.read(options.config_filename)
        g_CONFIG['connect_url'] = config.get("main", "connect_url")
        g_CONFIG['security_token'] = config.get("main", "security_token")
        g_CONFIG['forward_url'] = config.get("main", "forward_url")
        g_CONFIG['close_url'] = config.get("main", "close_url")
        try:
            g_CONFIG['socket_port'] = int(config.get("main", "http_port"))
        except:
            pass
        try:
            g_CONFIG['cluster_name'] = config.get("main", "cluster_name")
        except:
            g_CONFIG['cluster_name'] = ''
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        return False

    if getattr(options, 'port', None):
        g_CONFIG['socket_port'] = int(options.port)

    log.info(g_CONFIG)
    return True


def update_config():
    parser = get_parser()
    options, args = parser.parse_args()

    try:
        config = ConfigParser.SafeConfigParser()
        config.read(options.config_filename)
        g_CONFIG['connect_url'] = config.get("main", "connect_url")
        g_CONFIG['security_token'] = config.get("main", "security_token")
        g_CONFIG['forward_url'] = config.get("main", "forward_url")
        g_CONFIG['close_url'] = config.get("main", "close_url")
        try:
            g_CONFIG['socket_port'] = int(config.get("main", "http_port"))
        except:
            pass
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        return False

    if getattr(options, 'port', None):
        g_CONFIG['socket_port'] = int(options.port)

    log.info(g_CONFIG)
    return True


def param_signature():
    ts = int(time.time())
    nonce = random.randint(1000, 99999)
    sign_ele = [g_CONFIG['security_token'], str(ts), str(nonce)]
    sign_ele.sort()
    sign = sha1(''.join(sign_ele)).hexdigest()
    params = {'timestamp': ts, 'nonce': nonce, 'signature': sign}
    return params
