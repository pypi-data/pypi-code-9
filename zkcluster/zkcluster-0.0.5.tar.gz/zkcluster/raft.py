# coding: utf-8

"""Partial raft consensus algorithm.

Includes the leader/follower selection aspect.

Currently, the log part is omitted, as we are looking only at
"who is the leader?" for database status messages.  However, we might
want to do the log anyway and have that be the framework for the
DB status messages themselves, which would eliminate the possibility
of any disagreement in status message, though this would increase latency
in getting the fastest DB status as we need to wait for agreement that
messages can first be committed.

This algo rides on top of the "rpc / peer" model given in rpc.py / p2p.py,
and is otherwise agnostic of the transport system in use.


"""
import logging
import random
import time

from . import rpc
from . import p2p
from . import state as _state
from . import util
from .util import event

log = logging.getLogger(__name__)

BATCH_SIZE = 1


class RaftListener(object):
    def status_changed(self, rafthandler, status):
        pass


class RaftHandler(object):
    name = 'raft'

    # slower election timer when things are connected
    # in a stable state, to greatly reduce message overhead and CPU
    # (verified with top this thing burns a lot when it's running
    # faster)
    smooth_sailing_range = (10, 15)

    # fast election timers when things are changing, so we can
    # reelect a leader quickly.
    freakout_range = (.150, .300)

    election_timeout_range = smooth_sailing_range
    rpc_timeout = .5

    state = _state.StateMachine()
    START = state.START
    LEADER = state.new("LEADER")
    FOLLOWER = state.new("FOLLOWER")
    CANDIDATE = state.new("CANDIDATE")

    def __init__(self, service):
        self.service = service
        self.p2p = p2p.PeerRunner(self.service)
        self.p2p.speak_rpc(rpc_reg)

        event.event_listen(self.service, "before_listen", self.before_listen)
        self.service.memos['raft'] = self
        self.state.init_instance(self)
        self.state.add_listener(self, self._state_changed)
        self.async_suite = service.async_suite
        self.candidate_id = service.nodename
        self.current_term = 0
        self.voted_for = None
        self._sped_up_at = float("inf")
        self.election_timer = None
        self.current_leader = None
        self._monitor_lock = self.async_suite.lock()

        event.event_listen(self.p2p, "new_peer", self._new_peer)
        event.event_listen(self.p2p, "peer_connected", self._peer_connected)
        event.event_listen(
            self.p2p, "peer_disconnected", self._peer_disconnected)

    def _state_changed(self, target, old_state, new_state):
        self.dispatch.state_changed(self, old_state, new_state)

    @property
    def is_leader(self):
        return self.current_leader == self.candidate_id

    def _new_peer(self, peer):
        """event hook from p2p runner"""
        peer.memos['voted_for_us'] = False
        peer.memos['ping_due'] = 0
        peer.memos['vote_due'] = 0

    def _peer_connected(self, peer):
        self._speed_up()
        self._run_monitor()

    def _peer_disconnected(self, peer):
        # TODO: check if we should see if only the leader here
        self._speed_up()
        self._run_monitor()

    def _update_memo(self, key, value):
        for peer in self.p2p.peers:
            peer.memos[key] = value

    def before_listen(self, server):
        self._raft_started = time.time()
        self.FOLLOWER.go(self)
        self._monitor_greenlet = self.async_suite.spawn(self._monitor)

    def _monitor(self):
        while True:
            self._run_monitor()
            self.async_suite.sleep(float(self.election_timeout_range[0]) / 4)

    def _run_monitor(self):
        if not self._monitor_lock.acquire(False):
            return
        try:
            now = time.time()
            if self.FOLLOWER.current(self):
                if self.election_timer(now):
                    self.CANDIDATE.go(self)
                else:
                    # slow down election timer after some period
                    self._check_slowdown(now, 20)
            elif self.LEADER.current(self):
                # slow down election timer after some period that
                # is considerably longer than what the followers do
                self._check_slowdown(now, 60)
                for peer in self.p2p.peers:
                    if not peer.connected:
                        continue
                    if peer.memos['ping_due'] < now:
                        self.request_append_entries(peer, now)
            elif self.CANDIDATE.current(self):
                if self.election_timer(now):
                    self.CANDIDATE.go(self)
                else:
                    any_ = False
                    for peer in self.p2p.peers:
                        if not peer.connected:
                            continue
                        any_ = True
                        if peer.memos['vote_due'] < now:
                            self.request_vote_request(peer, now)
                    if not any_:
                        self._check_votes()
        finally:
            self._monitor_lock.release()

    def _reset_election_timer(self, fire=False):
        timeout = random.uniform(*self.election_timeout_range)
        now = time.time()
        if fire:
            # make the first hit very soon
            now -= self.election_timeout_range[0]
        self.election_timer = util.periodic_timer(timeout, now)

    def _speed_up(self):
        reset_timer = self._sped_up_at == float("inf")
        self._sped_up_at = time.time()
        if reset_timer:
            self.election_timeout_range = self.freakout_range
            self._reset_election_timer(fire=True)
            log.info(
                "Peer changes detected, speeding up "
                "election timeouts to %.4f" % self.election_timeout_range[0])

    def _check_slowdown(self, now, gap_factor):
        gap = self.freakout_range[-1] * gap_factor
        if now - self._sped_up_at > gap:
            self.election_timeout_range = self.smooth_sailing_range
            self._reset_election_timer()
            log.info(
                "Entering stable state, slowing down "
                "election timeouts to %.4f" % self.election_timeout_range[0])
            self._sped_up_at = float("inf")

    @state.transition(START, FOLLOWER)
    def _start_to_follower(self, from_, to):
        log.info("peer [%s] entering FOLLOWER state", self.candidate_id)
        self._update_memo("vote_due", 0)
        self._update_memo("ping_due", 0)
        self._reset_election_timer()

    @state.transition(FOLLOWER, CANDIDATE)
    def _follower_to_candidate(self, from_, to):
        self._speed_up()
        self.current_term += 1
        self.voted_for = self.candidate_id
        self._update_memo("voted_for_us", False)
        self._update_memo("ping_due", 0)
        self._update_memo("vote_due", 0)
        self._reset_election_timer()
        log.info(
            "peer [%s] moving from FOLLOWER -> CANDIDATE, "
            "starting new election for term %s, timeout %.4f",
            self.candidate_id,
            self.current_term, self.election_timer.interval)

    @state.transition(CANDIDATE, CANDIDATE, interesting=False)
    def _candidate_to_candidate(self, from_, to):
        self.current_term += 1
        self._update_memo("voted_for_us", False)
        self._update_memo("vote_due", 0)
        self._reset_election_timer()
        log.debug(
            "peer [%s] remains in CANDIDATE, starting election "
            "for new term %s, timeout %.4f",
            self.candidate_id, self.current_term, self.election_timer.interval)

    @state.transition(CANDIDATE, LEADER)
    def _candidate_to_leader(self, from_, to):
        self.current_leader = self.candidate_id
        log.info(
            "peer [%s] moving from CANDIDATE -> LEADER", self.candidate_id)
        self._update_memo("ping_due", 0)

    @state.transition(CANDIDATE, FOLLOWER)
    def _candidate_to_follower(self, from_, to, term):
        log.info(
            "peer [%s] moving from CANDIDATE -> FOLLOWER", self.candidate_id)
        self.voted_for = None
        self.current_term = term

    @state.transition(LEADER, FOLLOWER)
    def _leader_to_follower(self, from_, to, term):
        log.info(
            "peer [%s] moving from LEADER -> FOLLOWER", self.candidate_id)
        self.voted_for = None
        self.current_term = term

    state.null(FOLLOWER, FOLLOWER)

    # the construction of these methods is taken more or less directly
    # from https://github.com/ongardie/raftscope/blob/master/raft.js
    def request_append_entries(self, peer, now):
        log_rec = AppendEntries(
            self.current_term,
            self.candidate_id,
            0, 0, [], 0  # log values, fixed for an empty log
        )

        peer.memos['ping_due'] = now + self.rpc_timeout

        log_rec.send_async(
            peer.rpc_service,
            lambda response: self.handle_append_entries_response(
                log_rec, peer, response),
            lambda response: self.error_response(log_rec, peer, response),
            timeout=self.rpc_timeout
        )

    def handle_append_entries_request(self, request, peer):
        """Receive an AppendEntries RPC call."""

        success = False

        # they're ahead of us, we step down
        if self.current_term < request.term and self.LEADER.current(self):
            self.FOLLOWER.go(self, request.term)

        if self.current_term == request.term:
            if self.CANDIDATE.current(self):
                self.FOLLOWER.go(self, request.term)
            self.election_timer.reset(time.time())
            success = True
            self.current_leader = request.leader_id

        return self.current_term, success

    def handle_append_entries_response(self, append_entries, peer, response):
        peer.memos['ping_due'] = \
            time.time() + self.election_timeout_range[-1] / 2

        response_term, response_success = response

        if self.current_term < response_term:
            self.FOLLOWER.go(self, response_term)

    def request_vote_request(self, peer, now):
        # vote for self
        assert self.current_term
        vote = RequestVote(
            self.current_term,
            self.candidate_id,
            0, 0
        )
        peer.memos['vote_due'] = now + self.rpc_timeout
        vote.send_async(
            peer.rpc_service,
            lambda response: self.handle_request_vote_response(
                vote, peer, response),
            lambda response: self.error_response(vote, peer, response),
            timeout=self.rpc_timeout,
        )

    def handle_request_vote_request(self, request, peer):
        granted = False

        if self.current_term < request.term:
            self.FOLLOWER.go(self, request.term)

        if self.current_term == request.term and (
            self.voted_for is None or
            self.voted_for == request.candidate_id
        ):
            granted = True
            self.voted_for = peer.name

        return self.current_term, granted

    def handle_request_vote_response(self, vote_request, peer, response):
        peer.memos['vote_due'] = float("inf")

        response_term, response_granted = response
        if self.current_term < response_term:
            self.FOLLOWER.go(self, response_term)

        if self.CANDIDATE.current(self) and self.current_term == response_term:
            if response_granted:
                peer.memos['voted_for_us'] = True
                self._check_votes()

    def _check_votes(self):
        vote_count = self._get_vote_count()
        if vote_count + 1 > self.p2p.total_number_of_peers / 2:
            self.LEADER.go(self)

    def _get_vote_count(self):
        return sum([
            1 if peer.memos['voted_for_us'] else 0
            for peer in self.p2p.peers
        ])

    def error_response(self, rpc_msg, peer, exception):
        log.info(
            "Exception received from peer %s: %s",
            peer.their_nodename, exception)


class RaftEvents(util.EventListener):
    _dispatch_target = RaftHandler

    def state_changed(self, raft, old_status, new_status):
        pass


class RaftConsoleCommands(object):
    name = 'raft'

    def __init__(self, console):
        console.register_cmds_from(self)
        p2p.P2PConsoleCommands(console)
        self.rpc_service = console.speak_rpc(rpc_reg)

    def cmd_leader(self):
        return CurrentLeader().send(self.rpc_service)

rpc_reg = rpc.RPCReg()


@rpc_reg.call()
class CurrentLeader(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        raft = service_connection.server.memos['raft']
        return raft.current_leader


# p2p RPC commands, these are bi-directional

@rpc_reg.call('term', 'leader_id', 'prev_log_index',
              'prev_log_term', 'entries', 'leader_commit')
class AppendEntries(p2p.P2PRpc):
    def receive_peer_request(self, rpc, peer):
        raft = peer.handler.service.memos['raft']
        return raft.handle_append_entries_request(self, peer)


@rpc_reg.call('term', 'candidate_id', 'last_log_index', 'last_log_term')
class RequestVote(p2p.P2PRpc):
    def receive_peer_request(self, rpc, peer):
        raft = peer.handler.service.memos['raft']
        return raft.handle_request_vote_request(self, peer)

