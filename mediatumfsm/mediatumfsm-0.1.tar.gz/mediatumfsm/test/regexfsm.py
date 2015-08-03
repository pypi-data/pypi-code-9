# -*- coding: utf-8 -*-
from mediatumfsm.fsm import FSM, State, case, Goto, Stay, Stop

### predefined handler conditions

is_a = lambda m, _: m == "a"
is_fourth_a = lambda m, d: m == "a" and d == 3


class RegexFSM(FSM):
    """Parses the regex 'aaaa(.*)#' and replace upper letters by a star'
    """
    initial_data = 0
    initial_state_name = "A"

    ### states

    class A(State):
        """Skip exactly 4 a's"""
        @case(str, is_fourth_a)
        def finish_a(*_):
            return Goto(RegexFSM.Repeat), ""

        @case(str, is_a)
        def collect_a(msg, data):
            return Stay, data + 1

    class Repeat(State):
        """repeat until # is reached"""
        @case(str, lambda m, _: m == "#")
        def end(*_):
            return Stop

        @case(str)
        def any(m, d):
            if m.isupper():
                m = "*"
            return Goto(RegexFSM.Repeat), d + m

    ### some parsing helpers

    def parse(self, data):
        """Sends all chars of string `data` into the FSM.
        Returns the recognized string if no errors occur.
        :param data: string to parse
        :type data: str
        """
        for c in data:
            self.send(c)
            if self.stopped:
                return self.data

    def parse_gen(self, data):
        """Generator which skips the leading a's and returns the recognized string after each char.
        :param data: string to parse
        :type data: str
        """
        it = iter(data)
        while self.state != RegexFSM.Repeat:
            self.send(next(it))
        while not self.stopped:
            yield self.data
            self.send(next(it))
