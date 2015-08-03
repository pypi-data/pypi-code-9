# -*- coding: utf-8 -*-
import ast
from copy import copy
from inspect import isclass
import inspect
import logging
from mediatumfsm.compat import itervalues, iteritems, iterkeys
logg = logging.getLogger("fsm")


def _sort_handlers(handlers):
    handlers.sort(key=lambda h: h.__code__.co_firstlineno)
    handlers.sort(key=lambda h: 0 if h._condition else 1)
    handlers.sort(key=lambda h: h._pos)


def _check_handler_validity(handlers, msg_type, func):
    if msg_type in handlers:
        # check for duplicate handlers with same condition
        for h in handlers[msg_type]:
            if h._condition == func._condition:
                logg.warn("handler (without condition) for msg type %s already defined, ignoring it: %s",
                          msg_type, func)
                return False
    return True


class _StateMeta(type):
    def __init__(cls, name, bases, dct):
        handlers = {}
        for name, obj in iteritems(dct):
            if isinstance(obj, staticmethod):
                func = obj.__func__
                msg_type = getattr(func, "_message_type", None)
                if msg_type:
                    valid = _check_handler_validity(handlers, msg_type, func)
                    if valid:
                        h_for_msg_type = handlers.setdefault(msg_type, [])
                        h_for_msg_type.append(func)
        for h_for_msg_type in itervalues(handlers):
            _sort_handlers(h_for_msg_type)
        cls.handlers = handlers
        super(_StateMeta, cls).__init__(name, bases, dct)


class _FSMMeta(type):
    def __init__(cls, name, bases, dct):
        # get states from bases
        states = {}
        for base in bases:
            if type(base) == _FSMMeta:
                states.update(base.states)
        handlers = {}
        transition_actions = {}
        cls_module = inspect.getmodule(cls)
        for name, obj in iteritems(dct):
            if isclass(obj) and type(obj) == _StateMeta:
                obj.name = obj.__name__
                states[name] = obj
                # register state classes in module where FSM was defined
                setattr(cls_module, name, obj)
                if obj.__name__ == cls.initial_state_name:
                    cls.initial_state = obj
            elif isinstance(obj, staticmethod):
                func = obj.__func__
                # only transition handlers have a _src_state attrib
                src_state = getattr(func, "_src_state", None)
                if src_state:
                    dest_state = func._dest_state
                    transition_actions[(src_state, dest_state)] = func
                # handlers must be defined with @unhandled_case (_bound_to_state == False) here
                bound_to_state = getattr(func, "_bound_to_state", False)
                if bound_to_state:
                    raise Exception("case handler not allowed here, must be defined in state class!")
                msg_type = getattr(func, "_message_type", None)
                if msg_type:
                    h_for_msg_type = handlers.setdefault(msg_type, [])
                    h_for_msg_type.append(func)
        cls.states = states
        cls.state_names = list(iterkeys(states))
        for h_for_msg_type in itervalues(handlers):
            _sort_handlers(h_for_msg_type)
        cls.handlers = handlers
        cls.transition_actions = transition_actions
        super(_FSMMeta, cls).__init__(name, bases, dct)


### state changes

class _StateChange(object):
    pass
