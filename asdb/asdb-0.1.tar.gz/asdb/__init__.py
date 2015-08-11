import socket
import errno
import sys
from utils import port_path


def find_port(host="127.0.0.1", port=6950, search_limit=100):
    for i in xrange(search_limit):
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this_port = port + i
        try:
            _sock.bind((host, this_port))
        except socket.error as exc:
            if exc.errno in [errno.EADDRINUSE, errno.EINVAL]:
                continue
            raise
        else:
            save_port(this_port)
            return _sock, this_port
    else:
        raise NoAvailablePortException


def debugger():
    try:
        from celery import current_task
        print current_task
        if current_task:
            from celery.contrib.rdb import Rdb

            class Rdb2(Rdb):

                def get_avail_port(self, host, port_p, search_limit=100, skew=+0):
                    return find_port(host, port_p, search_limit)

            return Rdb2(port=6950)
    except ImportError:
        pass
    import rpdb
    sock, port = find_port()
    sock.close()
    return rpdb.Rpdb(port=port)


def save_port(port):
    path = port_path()
    with open(path, 'w') as portfile:
        portfile.write(str(port))
        portfile.flush()


def t():
    db = debugger()
    db.set_trace(sys._getframe(2))


class NoAvailablePortException(Exception):
    pass


t()

del sys.modules['asdb']
