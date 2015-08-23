from zymbit.common.config import *

FILES_ROOT = '/usr/files/arduino'
KNOWN_HOSTS = '/.ssh/known_hosts'

TUNNEL_SSH_KEY_PATH = os.path.expanduser(os.environ.get('TUNNEL_SSH_KEY_PATH', '/.ssh/id_tunnel'))

ZYMBIT_KNOWN_HOSTS = '/etc/dropbear/zymbit_known_hosts'
