import logging
import time

from zymbit.timeutil import now, get_sleep_time


class StateMachine(object):
    transitions = {}

    def __init__(self):
        self._run = True
        self._state = self.start

        self.loop_sleep_time = 1.0

        self._setup_transitions()
        self.logger.debug('transitions={}'.format(self.transitions))

    def _setup_transitions(self):
        # convert the transition functions into bound methods
        _transitions = {}
        for k, v in self.transitions.items():
            bound_method = getattr(self, k.func_name)
            t_transitions = dict([(kk, getattr(self, vv.func_name)) for kk, vv in v.items()])

            _transitions[bound_method] = t_transitions

        self.transitions = _transitions

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def get_new_state(self, transition_key):
        transitions = self.transitions.get(self._state, {})

        return transitions.get(transition_key)

    def loop(self):
        exc = None
        result = None

        try:
            result = self._state()
        except Exception, exc:  # global exception catcher here to use for state transitions
            self._state = self.get_new_state(exc) or self._state

            raise

        transitions = self.transitions.get(self._state, {})
        if result:
            self._state = transitions.get(result) or self._state

        return result

    def quit(self):
        self._run = False

    def run(self):
        while self._run:
            start = now()

            result = self.loop()
            if result is None:
                sleep_time = get_sleep_time(self.loop_sleep_time, start)
                # self.logger.debug('loop_sleep_time={}, sleep_time={}'.format(self.loop_sleep_time, sleep_time))
                time.sleep(sleep_time)

    def start(self):
        return True
