# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import time
from mediatumfsm.fsm import State, case, unhandled_case, on_transition, Stay, Goto
from mediatumfsm.sessionfsm import SessionFSM

logg = logging.getLogger("fsm")

def even(m, _):
    return m % 2 == 0

transition_log = {}

switched_to_int_times = 0

class Message(object):
    pass


class AcceptInt(Message):
    pass


class AcceptStr(Message):
    pass


class Accumulator(SessionFSM):
    initial_data = False
    initial_state_name = "Nothing"
    session = {}

    class Nothing(State):
        pass

    class Str(State):
        @case(AcceptStr)
        def nothing(*_):
            return Stay

        @case(str)
        def handle_str(message, data):
            print("string message:", message, "data", data)
            return Stay, data + message

    class Int(State):
        @case(AcceptInt)
        def nothing(*_):
            return Stay

        @case(int, even)
        def set_value_even_int(number, data):
            print("got even number")
            return Stay, (data[0] + number, "even")

        @case(int, lambda m, d: m % 2 == 1)
        def set_value_odd_int(number, data):
            print("got odd number")
            return Stay, (data[0] + number, "odd")

    # switching to Str and Int state is always allowed

    @unhandled_case(AcceptInt)
    def switch_to_int(*_):
        return Goto(Accumulator.Int), (0, None)

    @unhandled_case(AcceptStr)
    def switch_to_str(*_):
        return Goto(Accumulator.Str), ""

    @unhandled_case(int)
    def invalid_int(*_):
        raise ValueError("int not allowed here!")

    @on_transition(State, "Int")
    def switched_to_int(*_):
        global switched_to_int_times
        switched_to_int_times += 1
        print("switched to int accepting state!")

    @on_transition(State, State)
    def trace(msg, data, src_state, dest_state):
        transition_log[time.time()] = {"msg": msg, "data": data, "src_state": src_state, "dest_state": dest_state}
        logg.info("state transition from %s to %s on msg %s with data '%s'", src_state.name, dest_state.name, msg, data)
