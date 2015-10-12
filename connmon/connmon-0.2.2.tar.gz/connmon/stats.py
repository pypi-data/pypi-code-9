import collections
from zkcluster import util
import os
import logging


log = logging.getLogger(__name__)

ROLLBACK_ON_RETURN = 0
COMMIT_ON_RETURN = 1
CONNECT = 2
CLOSE = 3
CHECKOUT = 4
CHECKIN = 5
INVALIDATE = 6
RECYCLE = 7

PROCESS_ADDED = 8
PROCESS_REMOVED = 9
SUMMARY = 10

ConnectionEvent = collections.namedtuple(
    'ConnectionEvent', [
        'hostname', 'progname', 'pid', 'ppid',
        'tid', 'connection_id', 'timestamp', 'action'
    ]
)

ProcessEvent = collections.namedtuple(
    'ProcessEvent', [
        'remote_hostname', 'remote_progname', 'remote_pid',
        'action'
    ]
)

SummaryEvent = collections.namedtuple(
    'SummaryEvent', ['summary', 'action']
)


_lookup = ([ConnectionEvent] * 8) + ([ProcessEvent] * 2) + [SummaryEvent]


def evt_from_tuple(msg):
    return _lookup[msg[-1]](*msg)


class ConnectionStat(object):
    __slots__ = (
        'key', 'hostname', 'pid', 'connection_id',
        'checkedout', 'progname'
    )

    def __init__(self, hostname, pid, connection_id, checkedout, progname):
        self.key = "%s|%s|%s" % (hostname, pid, connection_id)
        self.hostname = hostname
        self.pid = pid
        self.connection_id = connection_id
        self.checkedout = checkedout
        self.progname = progname

    def summary(self):
        return (
            self.hostname, self.pid,
            self.connection_id, self.checkedout, self.progname)

    @classmethod
    def from_summary(self, summary):
        return ConnectionStat(*summary)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key


class HostProg(object):
    def __init__(self, hostname, progname):
        self.hostname = hostname
        self.progname = progname
        self.connections = {}
        self.checkedout = set()
        self.max_connections = 0
        self.max_checkedout = 0
        self.max_process_count = 0
        self.pids = set()

    def summary(self):
        return {
            "hostname": self.hostname,
            "progname": self.progname,
            "connections": dict(
                (key, conn.summary())
                for (key, conn) in self.connections.items()
            ),
            "checkedout": [conn.key for conn in self.checkedout],
            "max_connections": self.max_connections,
            "max_checkedout": self.max_checkedout,
            "max_process_count": self.max_process_count,
            "pids": list(self.pids)
        }

    def merge_summary(self, summary):
        self.connections.update(
            (key, ConnectionStat.from_summary(stat_summary))
            for key, stat_summary in summary['connections'].items(),
        )
        self.checkedout.update(
            self.connections[key] for key in summary['checkedout']
        )
        self.pids.update(summary['pids'])
        self.max_connections = max(
            summary['max_connections'],
            self.max_connections, len(self.connections))
        self.max_checkedout = max(
            summary['max_checkedout'],
            self.max_checkedout, len(self.checkedout))
        self.max_process_count = max(
            summary['max_process_count'],
            self.max_process_count, self.process_count)

    def connect(self, stat):
        self.connections[stat.key] = stat
        self.max_connections = max(self.max_connections, len(self.connections))

    def close(self, stat):
        del self.connections[stat.key]

    def checkout(self, stat):
        self.checkedout.add(stat)
        self.max_checkedout = max(self.max_checkedout, len(self.checkedout))

    def checkin(self, stat):
        self.checkedout.remove(stat)

    def invalidate(self, stat):
        self.checkedout.remove(stat)

    @property
    def short_progname(self):
        if self.progname:
            return os.path.basename(self.progname)
        else:
            return "<none>"

    @property
    def connection_count(self):
        return len(self.connections)

    @property
    def checkout_count(self):
        return len(self.checkedout)

    @property
    def process_count(self):
        return len(self.pids)

    def add_pid(self, remote_pid):
        self.pids.add(remote_pid)
        self.max_process_count = max(self.max_process_count, len(self.pids))

    def remove_pid(self, remote_pid):
        for key, value in list(self.connections.items()):
            if value.pid == remote_pid:
                del self.connections[key]
        self.pids.remove(remote_pid)


class Stats(object):
    def __init__(self, _green=False):
        self.hostprogs = {}
        self.async_suite = util.async_suite(green=_green)
        self.lock = self.async_suite.lock()

    @property
    def process_count(self):
        return sum(
            hostprog.process_count for hostprog in self.hostprogs.values()
        )

    @property
    def host_count(self):
        return len(
            set(hostprog.hostname
                for hostprog in self.hostprogs.values() if hostprog.pids)
        )

    @property
    def max_host_count(self):
        return len(
            set(hostprog.hostname for hostprog in self.hostprogs.values())
        )

    @property
    def max_process_count(self):
        return sum(
            hostprog.max_process_count for hostprog in self.hostprogs.values()
        )

    @property
    def connection_count(self):
        return sum(
            hostprog.connection_count for hostprog in self.hostprogs.values()
        )

    @property
    def checkout_count(self):
        return sum(
            hostprog.checkout_count for hostprog in self.hostprogs.values()
        )

    @property
    def max_connection_count(self):
        return sum(
            hostprog.max_connections for hostprog in self.hostprogs.values()
        )

    @property
    def max_checkout_count(self):
        return sum(
            hostprog.max_checkedout for hostprog in self.hostprogs.values()
        )

    def summary(self):
        return [host.summary() for host in self.hostprogs.values()]

    def _get_hostprog(self, remote_hostname, remote_progname):
        with self.lock:
            try:
                hostprog = self.hostprogs[(remote_hostname, remote_progname)]
            except KeyError:
                hostprog = \
                    self.hostprogs[(remote_hostname, remote_progname)] = \
                    HostProg(remote_hostname, remote_progname)
        return hostprog

    def summary_added(self, summary):
        evt = SummaryEvent(
            summary, SUMMARY
        )
        self.receive_message(evt)
        return evt

    def process_added(self, remote_hostname, remote_progname, remote_pid):
        evt = ProcessEvent(
            remote_hostname, remote_progname, remote_pid,
            PROCESS_ADDED
        )
        self.receive_message(evt)
        return evt

    def process_closed(self, remote_hostname, remote_progname, remote_pid):
        evt = ProcessEvent(
            remote_hostname, remote_progname, remote_pid,
            PROCESS_REMOVED
        )

        self.receive_message(evt)
        return evt

    def _process_added(self, message):
        hostprog = self._get_hostprog(
            message.remote_hostname, message.remote_progname)
        hostprog.add_pid(message.remote_pid)

    def _process_closed(self, message):
        try:
            hostprog = self.hostprogs[
                (message.remote_hostname, message.remote_progname)]
        except KeyError:
            pass
        else:
            hostprog.remove_pid(message.remote_pid)

    def _summary_added(self, message):
        summary = message.summary
        for hostprog_summary in summary:
            remote_hostname, remote_progname = \
                hostprog_summary['hostname'], hostprog_summary['progname']

            hostprog = self._get_hostprog(remote_hostname, remote_progname)
            hostprog.merge_summary(hostprog_summary)

    def receive_message(self, message):
        log.debug("message received: %s", message)

        if message.action == PROCESS_ADDED:
            self._process_added(message)
        elif message.action == PROCESS_REMOVED:
            self._process_closed(message)
        elif message.action == SUMMARY:
            self._summary_added(message)
        else:
            hostprog_key = message.hostname, message.progname
            conn_key = "%s|%s|%s" % (
                message.hostname, message.pid, message.connection_id)

            hostprog = self.hostprogs[hostprog_key]

            if message.action == CONNECT:
                hostprog.connect(
                    ConnectionStat(
                        message.hostname, message.pid, message.connection_id,
                        False, message.progname)
                )
            else:
                try:
                    stat = hostprog.connections[conn_key]
                except KeyError:
                    log.debug(
                        "Received message for unhandled connection %s; %s",
                        conn_key, message
                    )
                    assert conn_key not in hostprog.checkedout
                else:
                    if message.action == INVALIDATE:
                        hostprog.invalidate(stat)
                    elif message.action == CHECKOUT:
                        hostprog.checkout(stat)
                    elif message.action == CHECKIN:
                        hostprog.checkin(stat)
                    elif message.action == CLOSE:
                        hostprog.close(stat)


class QueuedStats(Stats):
    def __init__(self):
        super(QueuedStats, self).__init__(_green=True)
        self.listeners = set()
        self.queue = self.async_suite.queue()
        self.super_ = super(QueuedStats, self)

    def start(self):
        self.runner = self.async_suite.background_thread(self._process_queue)

    def _process_queue(self):
        while True:
            message = self.queue.get()
            self.super_.receive_message(message)
            self.dispatch.message_received(message)

    def receive_message(self, message):
        self.queue.put(message)


class StatsListener(util.EventListener):
    _dispatch_target = QueuedStats

    def message_received(self, message):
        pass

