import collections
import os
import math
import logging

from zkcluster import util

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
PROCESS_UPDATED = 10
DETAILED_SUMMARY = 11
SHALLOW_SUMMARY = 12

ConnectionEvent = collections.namedtuple(
    'ConnectionEvent', [
        'hostname', 'progname', 'pid', 'ppid',
        'tid', 'connection_id', 'timestamp', 'action'
    ]
)

ProcessEvent = collections.namedtuple(
    'ProcessEvent', [
        'remote_hostname', 'remote_progname', 'remote_pid',
        'payload', 'timestamp', 'action'
    ]
)

SummaryEvent = collections.namedtuple(
    'SummaryEvent', ['summary', 'action']
)


_lookup = ([ConnectionEvent] * 8) + ([ProcessEvent] * 3) + ([SummaryEvent] * 2)

_PERSECOND_SAMPLE = 10


def evt_from_tuple(msg):
    return _lookup[msg[-1]](*msg)


class ConnectionStat(object):
    """Represents an individual connection owned by a process on a host."""

    __slots__ = (
        'key', 'hostname', 'pid', 'connection_id', 'progname'
    )

    def __init__(self, hostname, pid, connection_id, progname):
        self.key = "%s|%s|%s" % (hostname, pid, connection_id)
        self.hostname = hostname
        self.pid = pid
        self.connection_id = connection_id
        self.progname = progname

    def summary(self):
        return (
            self.hostname, self.pid,
            self.connection_id, self.progname)

    @classmethod
    def from_summary(self, summary):
        return ConnectionStat(*summary)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key


class AbstractHostProg(object):
    """Represents a program running on the host."""

    def __init__(self, hostname, progname):
        self.hostname = hostname
        self.progname = progname
        self.max_process_count = 0
        self.max_connections = 0
        self.max_checkedout = 0
        self._checkouts_per_second = EvtPerSecond()

    @property
    def short_progname(self):
        if self.progname:
            return os.path.basename(self.progname)
        else:
            return "<none>"

    @property
    def connection_count(self):
        raise NotImplementedError()

    @property
    def checkout_count(self):
        raise NotImplementedError()

    @property
    def checkouts_per_second(self):
        raise NotImplementedError()

    @property
    def process_count(self):
        raise NotImplementedError()

    def detailed_summary(self):
        raise NotImplementedError()

    @property
    def has_pids(self):
        raise NotImplementedError()

    def shallow_summary(self):
        return {
            "type": "shallow",
            "hostname": self.hostname,
            "progname": self.progname,
            "connection_count": self.connection_count,
            "checkout_count": self.checkout_count,
            "process_count": self.process_count,
            "max_connections": self.max_connections,
            "max_checkedout": self.max_checkedout,
            "max_process_count": self.max_process_count,
            "checkouts_per_second": self._checkouts_per_second.summary(),
        }


class EvtPerSecond(object):
    __slots__ = 'prev_ts', 'prev_count', 'current_ts', 'current_count'

    GRANULARITY = 1
    "length of time in a sample"

    def __init__(self):
        self.prev_ts = 0
        self.prev_count = 0
        self.current_ts = 0
        self.current_count = 1

    def _normalize_ts(self, ts):
        return math.floor(ts) / EvtPerSecond.GRANULARITY

    def current(self, now):
        normalize_now = self._normalize_ts(now)
        if normalize_now - self.current_ts > self.current_ts - self.prev_ts:
            divisor = normalize_now - self.current_ts
            count = self.current_count
        else:
            divisor = self.current_ts - self.prev_ts
            count = self.prev_count

        return (count / divisor) / EvtPerSecond.GRANULARITY

    def event(self, timestamp):
        timestamp = self._normalize_ts(timestamp)

        if timestamp > self.current_ts:
            self.prev_ts, self.prev_count = self.current_ts, self.current_count
            self.current_ts, self.current_count = timestamp, 1
        elif timestamp < self.prev_ts:
            # event happened in the past, discard
            pass
        elif timestamp == self.current_ts:
            self.current_count += 1
        else:
            self.prev_count += 1

    def summary(self):
        return {
            "prev_ts": self.prev_ts,
            "prev_count": self.prev_count,
            "current_ts": self.current_ts,
            "current_count": self.current_count
        }

    def merge_from_summary(self, summary):
        self.prev_ts = summary['prev_ts']
        self.prev_count = summary['prev_count']
        self.current_ts = summary['current_ts']
        self.current_count = summary['current_count']


class AbstractPidInfo(object):
    __slots__ = 'pid', 'connections', 'checkedout', 'max_connections', \
        'max_checkedout'

    def __init__(self, pid):
        self.pid = pid
        self.max_connections = 0
        self.max_checkedout = 0
        self.connections = {}
        self.checkedout = set()

    def __hash__(self):
        return self.pid

    def __eq__(self, other):
        return other.pid == self.pid

    @classmethod
    def from_summary(cls, summary):
        pid = cls(
            summary['pid']
        )
        pid.connections.update(
            (key, ConnectionStat.from_summary(stat_summary))
            for key, stat_summary in summary['connections'].items(),
        )
        pid.checkedout.update(
            pid.connections[key] for key in summary['checkedout']
        )
        pid.max_connections = summary['max_connections']
        pid.max_checkedout = summary['max_checkedout']
        return pid

    def summary(self):
        return {
            "pid": self.pid,
            "connections": dict(
                (key, conn.summary())
                for (key, conn) in self.connections.items()
            ),
            "checkedout": [conn.key for conn in self.checkedout],
            "max_connections": self.max_connections,
            "max_checkedout": self.max_checkedout,
        }

    def connect(self, stat, timestamp):
        self.connections[stat.key] = stat
        self.max_connections = max(self.max_connections, len(self.connections))

    def close(self, stat, timestamp):
        assert stat not in self.checkedout
        del self.connections[stat.key]

    def checkout(self, stat, timestamp):
        self.checkedout.add(stat)
        self.max_checkedout = max(self.max_checkedout, len(self.checkedout))

    def checkin(self, stat, timestamp):
        self.checkedout.remove(stat)

    def invalidate(self, stat, timestamp):
        self.checkedout.remove(stat)

    @property
    def connection_count(self):
        return len(self.connections)

    @property
    def checkout_count(self):
        return len(self.checkedout)


class PidInfo(AbstractPidInfo):
    """Represent pid information within a DetailedHostProg tracked by
    the server.

    """
    def __init__(self, pid):
        super(PidInfo, self).__init__(pid)


class RemotePid(AbstractPidInfo):
    """Receive originating stats messages on behalf of a single host / pid.

    RemotePid sits with the StatsClient and ConnectionPoolAnalyzer in
    a process that's reporting on its use of an SQLAlchemy Engine.
    It maintains a collection of ConnectionStat objects on behalf of that
    process id.  A summary of the object as well as ongoing events are sent
    to the stats server, where the data represented by this RemotePid becomes
    that of a single PidInfo inside of a DetailedHostProg instance.

    """

    __slots__ = 'hostname', 'progname'

    def __init__(self, hostname, progname, pid):
        self.hostname = hostname
        self.progname = progname
        super(RemotePid, self).__init__(pid)

    def receive_message(self, message):
        log.debug("message received: %s", message)

        if message.connection_id is None:
            log.debug("Received message with None for connection %s", message)
            return

        conn_key = "%s|%s|%s" % (
            message.hostname, message.pid, message.connection_id)

        assert message.hostname == self.hostname
        assert message.pid == self.pid

        if message.action == CONNECT:
            self.connect(
                ConnectionStat(
                    message.hostname, message.pid, message.connection_id,
                    message.progname),
                message.timestamp
            )
        else:
            try:
                stat = self.connections[conn_key]
            except KeyError:
                log.debug(
                    "Received message for unhandled connection %s; %s",
                    conn_key, message
                )
                assert conn_key not in self.checkedout
            else:
                if message.action == INVALIDATE:
                    self.invalidate(stat, message.timestamp)
                elif message.action == CHECKOUT:
                    self.checkout(stat, message.timestamp)
                elif message.action == CHECKIN:
                    self.checkin(stat, message.timestamp)
                elif message.action == CLOSE:
                    self.close(stat, message.timestamp)
                else:
                    assert False

    def detailed_summary(self):
        return [
            {
                "type": "detailed",
                "hostname": self.hostname,
                "progname": self.progname,
                "max_connections": self.max_connections,
                "max_checkedout": self.max_checkedout,
                "max_process_count": 1,
                "pids": [self.summary()]
            }
        ]


class DetailedHostProg(AbstractHostProg):
    """Represents a program running on the host with detailed pid
    and connection information.

    DetailedHostProg stores a collection of PidInfo objects
    each of which maintains a collection of ConnectionStat objects,
    each representing a database connection within a process.
    The object is only present in the stats server.

    The top-level summarization provided by a DetailedHostProg is passed
    from the server to ShallowHostProg instances that are maintained by
    console sessions.

    """
    def __init__(self, hostname, progname):
        super(DetailedHostProg, self).__init__(hostname, progname)
        self.pids = {}

    def detailed_summary(self):
        return {
            "type": "detailed",
            "hostname": self.hostname,
            "progname": self.progname,
            "max_connections": self.max_connections,
            "max_checkedout": self.max_checkedout,
            "max_process_count": self.max_process_count,
            "checkouts_per_second": self._checkouts_per_second.summary(),
            "pids": [pid.summary() for pid in self.pids.values()]
        }

    def merge_summary(self, summary):
        assert summary["type"] == "detailed"
        self.pids.update(
            (pid_summary['pid'], PidInfo.from_summary(pid_summary))
            for pid_summary in summary['pids']
        )
        self.max_process_count = max(
            summary['max_process_count'],
            self.max_process_count, self.process_count)
        self.max_connections = max(self.max_connections, self.connection_count)
        self.max_checkedout = max(self.max_checkedout, self.checkout_count)
        if "checkouts_per_second" in summary:
            self._checkouts_per_second.merge_from_summary(
                summary["checkouts_per_second"])

    def connect(self, stat, timestamp):
        pid = self.pids[stat.pid]
        pid.connect(stat, timestamp)
        self.max_connections = max(self.max_connections, self.connection_count)

    def close(self, stat, timestamp):
        self.pids[stat.pid].close(stat, timestamp)

    def checkout(self, stat, timestamp):
        pid = self.pids[stat.pid]
        pid.checkout(stat, timestamp)
        self._checkouts_per_second.event(timestamp)
        self.max_checkedout = max(self.max_checkedout, self.checkout_count)

    def checkin(self, stat, timestamp):
        self.pids[stat.pid].checkin(stat, timestamp)

    def invalidate(self, stat, timestamp):
        self.pids[stat.pid].invalidate(stat, timestamp)

    def checkouts_per_second(self, now):
        return self._checkouts_per_second.current(now)

    @property
    def has_pids(self):
        return bool(self.pids)

    @property
    def connection_count(self):
        return sum(pid.connection_count for pid in self.pids.values())

    @property
    def checkout_count(self):
        return sum(pid.checkout_count for pid in self.pids.values())

    @property
    def process_count(self):
        return len(self.pids)

    def add_pid(self, remote_pid):
        self.pids[remote_pid] = PidInfo(remote_pid)
        self.max_process_count = max(self.max_process_count, len(self.pids))

    def remove_pid(self, remote_pid):
        del self.pids[remote_pid]


class ShallowHostProg(AbstractHostProg):
    """Represents a program running on a host with only summaries of
    numbers of processes / connections / checkouts.

    ShallowHostProg only stores counts and stats for the given program / host
    but does not accommodate pid or connection events; it only displays
    data that ultimately was collected by a DetailedHostProg elsewhere.

    """

    def __init__(self, hostname, progname):
        super(ShallowHostProg, self).__init__(hostname, progname)
        self._connection_count = 0
        self._checkout_count = 0
        self._process_count = 0

    def merge_summary(self, summary):
        assert summary["type"] == "shallow"
        self._process_count = summary["process_count"]
        self._connection_count = summary["connection_count"]
        self._checkout_count = summary["checkout_count"]
        self._checkouts_per_second.merge_from_summary(
            summary["checkouts_per_second"])
        self.max_connections = summary["max_connections"]
        self.max_checkedout = summary["max_checkedout"]
        self.max_process_count = summary["max_process_count"]

    @property
    def has_pids(self):
        return self._process_count > 0

    @property
    def connection_count(self):
        return self._connection_count

    @property
    def checkout_count(self):
        return self._checkout_count

    @property
    def process_count(self):
        return self._process_count

    def checkouts_per_second(self, now):
        return self._checkouts_per_second.current(now)


class QueuedStats(object):
    """Represent data gathered over a series of hosts / pids / connections.

    QueuedStats sits both within a server as well as in a console.
    The "shallow" version is console oriented and only collects ShallowHostProg
    instances.  The "deep" version is used by the server and collects
    DetailedHostProg instance, which in turn contain PidInfo and ConnectionStat
    objects representing everything about a certain process on a host.

    """
    def __init__(self, _green=False, shallow=False):
        self.hostprogs = {}
        self.async_suite = util.async_suite(green=_green)
        self.lock = self.async_suite.lock()
        self.shallow = shallow
        self.listeners = set()
        self.queue = self.async_suite.queue()
        self.receive_mutex = self.async_suite.lock()

    def start(self):
        self.runner = self.async_suite.background_thread(self._process_queue)

    @property
    def process_count(self):
        return sum(
            hostprog.process_count for hostprog in self.hostprogs.values()
        )

    @property
    def host_count(self):
        return len(
            set(hostprog.hostname
                for hostprog in self.hostprogs.values() if hostprog.has_pids)
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
    def max_connections(self):
        return sum(
            hostprog.max_connections for hostprog in self.hostprogs.values()
        )

    @property
    def max_checkedout(self):
        return sum(
            hostprog.max_checkedout for hostprog in self.hostprogs.values()
        )

    def checkouts_per_second(self, now):
        entries = [
            host.checkouts_per_second(now)
            for host in self.hostprogs.values()
        ]
        return sum(entries)

    def shallow_summary(self):
        return [host.shallow_summary() for host in self.hostprogs.values()]

    def detailed_summary(self):
        return [host.detailed_summary() for host in self.hostprogs.values()]

    def receive_message(self, message):
        self.queue.put(message)

    def _process_queue(self):
        while True:
            message = self.queue.get()
            self._handle_message(message)

    def _handle_message(self, message):
        log.debug("message received: %s", message)

        self.dispatch.message_received(message)

        if message.action == PROCESS_ADDED:
            self._process_added(message)
        elif message.action == PROCESS_REMOVED:
            self._process_closed(message)
        elif message.action == PROCESS_UPDATED:
            self._process_updated(message)
        elif message.action == DETAILED_SUMMARY:
            self._detailed_summary_added(message)
        elif message.action == SHALLOW_SUMMARY:
            self._shallow_summary_added(message)
        else:
            self._handle_connection_event(message)

    def _get_hostprog(self, remote_hostname, remote_progname):
        with self.lock:
            try:
                hostprog = self.hostprogs[(remote_hostname, remote_progname)]
            except KeyError:
                hostprog = \
                    self.hostprogs[(remote_hostname, remote_progname)] = \
                    DetailedHostProg(remote_hostname, remote_progname) \
                    if not self.shallow \
                    else ShallowHostProg(remote_hostname, remote_progname)
        return hostprog

    def _process_added(self, message):
        if self.shallow:
            raise NotImplementedError("only supported for non shallow stats")
        hostprog = self._get_hostprog(
            message.remote_hostname, message.remote_progname)
        hostprog.add_pid(message.remote_pid)
        self.dispatch.hostprog_modified(hostprog)

    def _process_closed(self, message):
        if self.shallow:
            raise NotImplementedError("only supported for non shallow stats")
        try:
            hostprog = self.hostprogs[
                (message.remote_hostname, message.remote_progname)]
        except KeyError:
            pass
        else:
            hostprog.remove_pid(message.remote_pid)
            self.dispatch.hostprog_modified(hostprog)

    def _process_updated(self, message):
        if not self.shallow:
            raise NotImplementedError("only supported for shallow stats")
        hostprog = self._get_hostprog(
            message.remote_hostname, message.remote_progname)
        hostprog.merge_summary(message.payload)
        self.dispatch.hostprog_modified(hostprog)

    def _detailed_summary_added(self, message):
        if self.shallow:
            raise NotImplementedError("only supported for non shallow stats")
        summary = message.summary
        for hostprog_summary in summary:
            remote_hostname, remote_progname = \
                hostprog_summary['hostname'], hostprog_summary['progname']

            hostprog = self._get_hostprog(remote_hostname, remote_progname)
            hostprog.merge_summary(hostprog_summary)
            self.dispatch.hostprog_modified(hostprog)

    def _shallow_summary_added(self, message):
        if not self.shallow:
            raise NotImplementedError("only supported for shallow stats")
        summary = message.summary
        for hostprog_summary in summary:
            remote_hostname, remote_progname = \
                hostprog_summary['hostname'], hostprog_summary['progname']

            hostprog = self._get_hostprog(remote_hostname, remote_progname)
            hostprog.merge_summary(hostprog_summary)
            self.dispatch.hostprog_modified(hostprog)

    def _handle_connection_event(self, message):
        if self.shallow:
            raise NotImplementedError("only supported for non shallow stats")
        if message.connection_id is None:
            log.debug("Received message with None for connection %s", message)
            return

        hostprog_key = message.hostname, message.progname

        conn_key = "%s|%s|%s" % (
            message.hostname, message.pid, message.connection_id)

        hostprog = self.hostprogs[hostprog_key]

        if message.action == CONNECT:
            hostprog.connect(
                ConnectionStat(
                    message.hostname, message.pid, message.connection_id,
                    message.progname),
                message.timestamp
            )
        else:
            try:
                stat = hostprog.pids[message.pid].connections[conn_key]
            except KeyError:
                # ensure that the pid for this key has been cleaned out
                if message.pid in hostprog.pids:
                    log.error(
                        "pid %s is still present in hostprog collection "
                        "however connection %s is unhandled, message: %s",
                        message.pid, conn_key, message)
            else:
                if message.action == INVALIDATE:
                    hostprog.invalidate(stat, message.timestamp)
                elif message.action == CHECKOUT:
                    hostprog.checkout(stat, message.timestamp)
                elif message.action == CHECKIN:
                    hostprog.checkin(stat, message.timestamp)
                elif message.action == CLOSE:
                    hostprog.close(stat, message.timestamp)
                else:
                    assert False
        self.dispatch.hostprog_modified(hostprog)


class StatsListener(util.EventListener):
    _dispatch_target = QueuedStats

    def message_received(self, message):
        pass

    def hostprog_modified(self, hostprog):
        pass
