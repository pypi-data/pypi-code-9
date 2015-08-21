import time
import gevent
import slogging
from protocol import P2PProtocol
log = slogging.get_logger('ctxmonitor')


class ConnectionMonitor(gevent.Greenlet):
    ping_interval = 1.
    response_delay_threshold = 2.
    max_samples = 10

    def __init__(self, proto):
        assert isinstance(proto, P2PProtocol)
        gevent.Greenlet.__init__(self)
        self.proto = proto
        self.samples = []
        self.last_request = time.time()
        self.last_response = time.time()

    def __repr__(self):
        return '<ConnectionMonitor(r)>'

    def track_request(self):
        self.last_request = time.time()

    def track_response(self):
        self.last_response = time.time()
        dt = self.last_response - self.last_request
        self.samples.append(dt)
        if len(self.samples) > self.max_samples:
            self.samples.pop(0)

    @property
    def last_response_elapsed(self):
        return time.time() - self.last_response

    @property
    def latency(self, num_samples=0):
        if not self.samples:
            return None
        num_samples = min(num_samples or self.max_samples, len(self.samples))
        return sum(self.samples[:num_samples]) / num_samples

    def _run(self):
        log.debug('p2p.peer.monitor.started', monitor=self)
        while True:
            log.debug('p2p.peer.monitor.pinging', monitor=self)
            self.proto.send_ping()
            gevent.sleep(self.ping_interval)
            log.debug('p2p.peer.monitor.latency', monitor=self, latency=self.latency)
            if self.last_response_elapsed > self.response_delay_threshold:
                log.debug('p2p.peer.monitor.unresponsive_peer', monitor=self)
                self.stop()

    def stop(self):
        self.kill()
