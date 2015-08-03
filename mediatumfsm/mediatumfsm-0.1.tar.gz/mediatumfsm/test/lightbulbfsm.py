# -*- coding: utf-8 -*-
from mediatumfsm.fsm import FSM, State, case, Goto, unhandled_case

class Message(object):
    pass

class SwitchOn(Message):
    pass

class SwitchOff(Message):
    pass

class Smash(Message):
    pass


electricity = False


class LightBulb(FSM):
    initial_state = "Off"

    class Off(State):
        @case(SwitchOn, electricity)
        def on(*_):
            return Goto(LightBulb.On)

    class On(State):
        @case(SwitchOff)
        def off(*_):
            return Goto(LightBulb.Off)

    class Broken(State):
        pass

    @unhandled_case(Smash)
    def break_it(m, d):
        return Goto(LightBulb.Broken), d
