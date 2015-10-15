import logging
import operator

log = logging.getLogger(__name__)


class State(object):
    def __init__(self, machine, name):
        self.machine = machine
        self.name = name

    def __str__(self):
        return "[%s]" % self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        try:
            return other.name == self.name
        except AttributeError:
            return False

    def current(self, target):
        inst = statemachine(target)
        return inst.state is self

    def go(self, target, *arg, **kw):
        inst = statemachine(target)
        return inst._go_target(target, self, *arg, **kw)

statemachine = operator.attrgetter("statemachine")


class StateMachine(object):
    def __init__(self):
        self._transitions = {}
        self._symbols = {}
        self._max_symbol_size = 0
        self.START = self.new("START")

    _BOUNCED = object()

    def new(self, sname):
        assert sname not in self._symbols, "name %s already exists" % sname
        self._symbols[sname] = state = State(self, sname)
        self._max_symbol_size = max(self._max_symbol_size, len(sname))
        return state

    def _null_transition(self, instance, from_, to, *arg, **kw):
        pass

    def init_instance(self, target):
        inst = StateMachineInstance(self, target)
        target.statemachine = inst
        return inst

    def add_listener(self, target, listener):
        statemachine(target).add_listener(listener)

    def get(self, target):
        inst = statemachine(target)
        return inst.state

    def str(self, target):
        inst = statemachine(target)
        return str(inst)

    def null(self, from_, to, **kw):
        """Mark a transition as it should pass silently."""
        self.transition(from_, to, **kw)(self._null_transition)

    def bounce(self, from_, to, **kw):
        """Mark a transition as that it should "bounce" back, not move."""
        self.transition(from_, to, **kw)(self._BOUNCED)

    def transition(self, from_, to, interesting=True):
        assert (from_, to) not in self._transitions, \
            "transition %s->%s already exists" % (from_, to)

        def go(fn):
            self._transitions[(from_, to)] = (fn, interesting)
            return fn
        return go


class StateMachineInstance(object):
    __slots__ = 'machine', 'state', 'log', '_transition', '_listeners'

    def __init__(self, machine, target):
        self.machine = machine
        self.state = machine.START
        self.log = logging.getLogger(target.__module__)
        self._transition = False
        self._listeners = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def _go_target(self, target, state, *arg, **kw):
        try:
            (fn, interesting) = self.machine._transitions[(self.state, state)]

            if fn is self.machine._BOUNCED:
                if interesting:
                    log.debug(
                        "%s: %s -> %s -> bounced -> %s",
                        target, self.state, state, self.state)
                return

        except KeyError:
            raise KeyError("Unknown transition: %s->%s" % (self.state, state))
        else:
            assert not self._transition, "reentrant state change call!"

            old_state = self.state
            if interesting:
                log.debug("%s: %s -> %s", target, old_state, state)
            try:
                self._transition = True
                ret = fn(target, old_state, state, *arg, **kw)
            except Exception:
                raise
            else:
                self.state = state
                for listener in self._listeners:
                    listener(target, old_state, state)
                return ret
            finally:
                self._transition = False

    def __str__(self):
        return str(self.state)


