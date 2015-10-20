import logging
import re
import socket
import subprocess

import six

from whaleapi.utils.config import get_os

VALID_HOSTNAME_RFC_1123_PATTERN = re.compile(r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")  # noqa
MAX_HOSTNAME_LEN = 255

log = logging.getLogger(__name__)


def is_valid_hostname(hostname):
    if hostname.lower() in {'localhost', 'localhost.localdomain', 'localhost6.localdomain6',
                            'ip6-localhost'}:
        log.warning("Hostname: %s is local" % hostname)
        return False
    if len(hostname) > MAX_HOSTNAME_LEN:
        log.warning("Hostname: %s is too long (max length is  %s characters)"
                    % (hostname, MAX_HOSTNAME_LEN))
        return False
    if VALID_HOSTNAME_RFC_1123_PATTERN.match(hostname) is None:
        log.warning("Hostname: %s is not complying with RFC 1123" % hostname)
        return False
    return True


def get_hostname():
    """
    Get the canonical host name this agent should identify as. This is
    the authoritative source of the host name for the agent.
    Tries, in order:
      * 'hostname -f' (on unix)
      * socket.gethostname()
    """

    hostname = None

    if hostname is None:
        def _get_hostname_unix():
            try:
                p = subprocess.Popen(['/bin/hostname', '-f'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                if p.returncode == 0:
                    if six.PY3:
                        return out.decode("utf-8").strip()
                    else:
                        return out.strip()
            except Exception:
                return None

        os_name = get_os()
        if os_name in ['mac', 'freebsd', 'linux', 'solaris']:
            unix_hostname = _get_hostname_unix()
            if unix_hostname and is_valid_hostname(unix_hostname):
                hostname = unix_hostname

    if hostname is None:
        try:
            socket_hostname = socket.gethostname()
        except socket.error:
            socket_hostname = None
        if socket_hostname and is_valid_hostname(socket_hostname):
            hostname = socket_hostname

    if hostname is None:
        log.critical("Unable to reliably determine host name.")
        raise Exception("Unable to reliably determine host name.")
    else:
        return hostname
