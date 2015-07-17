import os
from walt.node.const import SERVER_LOGS_FIFO
from walt.node.tools import lookup_server_ip
from walt.common.tools import failsafe_mkfifo
from walt.common.logs import LogsConnectionToServer

class LogsFileMonitor(object):
    server_ip = lookup_server_ip()
    def __init__(self, stream_name, path):
        self.f = open(path, 'r')
        self.conn = LogsConnectionToServer(
                    LogsFileMonitor.server_ip)
        self.conn.start_new_incoming_logstream(stream_name)

    # let the event loop know what we are reading on
    def fileno(self):
        return self.f.fileno()

    # when the event loop detects an event for us,
    # read the log line and process it
    def handle_event(self, ts):
        line = self.f.readline()
        if line == '':  # empty read
            return False # remove from loop
        self.conn.log(line=line.strip(), timestamp=ts)

    def close(self):
        self.conn.close()
        self.f.close()

class LogsFifoServer(object):
    def __init__(self):
        failsafe_mkfifo(SERVER_LOGS_FIFO)
        self.fifo = open(SERVER_LOGS_FIFO, 'r')

    def join_event_loop(self, ev_loop):
        self.ev_loop = ev_loop
        ev_loop.register_listener(self)

    # let the event loop know what we are reading on
    def fileno(self):
        return self.fifo.fileno()

    # when the event loop detects an event for us,
    # read the request and process it
    def handle_event(self, ts):
        req = self.fifo.readline().split()
        if req[0] == 'MONITOR':
            listener = LogsFileMonitor(*req[1:])
            ev_loop.register_listener(listener)

    def close(self):
        self.fifo.close()

