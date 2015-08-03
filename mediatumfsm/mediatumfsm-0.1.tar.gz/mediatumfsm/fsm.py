# -*- coding: utf-8 -*-
import ast
from copy import deepcopy
from collections import Sequence
import inspect
import logging
import sys
import textwrap

from mediatumfsm._fsm import _StateMeta, _FSMMeta, _StateChange
from mediatumfsm.compat import itervalues, iteritems, iterkeys, with_metaclass
from itertools import chain


logg = logging.getLogger("fsm")

try:
    from pydot import Node, Edge, Dot
except ImportError:
    logg.warn("pydot not found. State Machine Diagrams won't work!")

### fsm exceptions

class FSMException(Exception):
    pass


class MessageNotAccepted(ValueError, FSMException):
    def __init__(self, rejected_message, current_state, allowed_messages):
        self.rejected_message = rejected_message
        self.allowed_messages = allowed_messages
        msg = "message {} {} in state {} not accepted. Accepted messages are: {}".format(
            rejected_message, rejected_message.__class__, current_state.name, allowed_messages)
        ValueError.__init__(self, msg)


class WrongResultType(ValueError, FSMException):
    def __init__(self, result, expected_result_type):
        msg = "wrong result {} : ({}), only instances of {} allowed!".format(
                                    result, result.__class__.__name__, expected_result_type)
        ValueError.__init__(self, msg)


def _match_handlers(handlers, message, data):
    try:
        handlers_for_msg_type = handlers[message.__class__]
    except KeyError:
        return None
    for h in handlers_for_msg_type:
        if h._condition is None or h._condition(message, data):
            logg.debug("handler %s matches", h)
            return h(message, data)

### state base class


class State(with_metaclass(_StateMeta)):
    """Subclass this to define your states. Must be an inner class in a FSM subclass.
    """
    @classmethod
    def set_action(cls, action):
        """Set callable which is used when FSM is in this state and fsm.action() is called.
        """
        cls.action = staticmethod(action)

    @staticmethod
    def action(*args, **kwargs):
        """Default: do nothing when fsm.action() is called
        """
        pass

    @classmethod
    def on_message(cls, message, data):
        """Called by FSM base class to handle messages in this state.
        """
        return _match_handlers(cls.handlers, message, data)


class End(State):
    """State which is reached when FSM is stopped.
    It's not possible to escape from this state.a
    """
    pass

### state changes

class Stay(_StateChange):
    pass

class Goto(_StateChange):
    def __init__(self, to):
        self.to = to

class Stop(_StateChange):
    def __init__(self, reason, data=None):
        self.reason = reason
        self.data = data

###  helpers for FSM


### FSM base

class FSM(with_metaclass(_FSMMeta)):
    """Subclass this to specify your FSM.
    The base FSM defines an End state which is inherited by all FSMs.
    Required:
      * override `initial_state_name` in your subclass to set the state which is used when a fresh FSM instance is created
    Optional:
      * override data_cls to restrict the FSM state data object to a certain type (or subclasses of the type)
    """
    initial_state_name = None
    initial_state = None # set automatically, do not override!
    data_cls = None # can be overriden
    End = End # default End state which is set when the FSM stops

    def __init__(self, state=None, data=None, name=None, fail_on_wrong_msg=True):
        """Initialize the state machine and set given state and data, if given.
        :param state: State to set FSM to. If None, use specified state given by `initial_state_name`.
        :param data: Initial state data. If None, use a copy of `initial_data`.
        :param name: Set a name for this FSM instance. Optional.
        :param fail_on_wrong_msg: True: Throw an exception if wrong messages (i.e. not accepted in current state) are sent to the FSM.
                                  False means that wrong msg are ignored.
        """
        self.fail_on_wrong_msg = fail_on_wrong_msg
        self.name = name
        self._graph = None
        if isinstance(state, str):
            try:
                state = self.states[state]
            except KeyError:
                raise ValueError("Unknown state {}, allowed states are {}".format(state, self.states))
        self.state = state if state else self.initial_state
        if data:
            self.data = data
        else:
            self.data = deepcopy(self.initial_data) if hasattr(self, "initial_data") else None


    def reset(self):
        """Reset the FSM to initial state and state data given in the FSM subclass."""
        self.state = self.initial_state
        self.data = deepcopy(self.initial_data) if hasattr(self, "initial_data") else None

    def _consume_handler_result(self, result):
        if not isinstance(result, Sequence):
            state_change = result
        elif len(result) == 2:
            state_change, new_data = result
            if new_data != self.data:
                if self.data_cls and new_data is not None and not isinstance(new_data, self.data_cls):
                    raise WrongResultType(new_data, self.data_cls)
                if logg.isEnabledFor(logging.DEBUG):
                    logg.debug("new data: %s", new_data)
                self.data = new_data
        else:
            raise NotImplementedError(result)
        if state_change == Stay or isinstance(state_change, Stay):
            logg.debug("no state change")
            return
        elif isinstance(state_change, Goto):
            logg.debug("transition from %s to %s", self.state, state_change.to)
            self.state = state_change.to
        elif state_change == Stop:
            logg.debug("finished")
            self.state = End
        elif isinstance(state_change, Stop):
            stop = state_change
            self.state = End
            logg.debug("finished, reason was %s, data %s", stop.reason, stop.data)
        else:
            raise NotImplementedError(state_change)
        return self.state

    def save_state(self):
        """Override this to specify how the current state and state data are saved in FSM.send() after message handling.
        See `SessionFSM` for an example how to save to a Flask-like Session object.
        """
        pass

    def send(self, message):
        """Send message to FSM and try to match handlers.
        First, all @case handlers in the current state are matched witch the given message and current state data.
        If no handler from the state matches, the @unhandled_case handlers specified for this FSM are tried.
        :param message: FSM message
        :throws MessageNotAccepted: Thrown if `self.fail_on_wrong_msg` is True and no handler matches.
        :throws WrongResultType: Thrown if `data_cls` is set and result type doesn't match `data_cls`.
        """
        logg.debug("got msg %s, current state %s with data %s", message, self.state.name, self.data)
        result = self.state.on_message(message, self.data)
        if result is None:
            # msg unhandled by state, try @unhandled_case common handlers
            result = _match_handlers(self.handlers, message, self.data)
            # still None?
            if result is None:
                if self.fail_on_wrong_msg:
                    raise MessageNotAccepted(message, self.state, self.accepted_messages)
                else:
                    return
        old_state = self.state
        new_state = self._consume_handler_result(result)
        if new_state:
            # run transition handlers
            for transition in ((State, State),
                               (State, new_state.__name__),
                               (old_state.__name__, State),
                               (old_state.__name__, new_state.__name__)):
                handler = self.transition_actions.get(transition)
                if handler:
                    handler(message, self.data, old_state, new_state)
        self.save_state()
        return new_state

    def _analyze_handler(self, h):
        # fix for the stupid code parser in inspect module...
        source, start = inspect.findsource(h)
        if "lambda" in source[start]:
            func_code = source[start] + "".join(inspect.getblock(source[start+1:]))
        else:
            func_code = "".join(inspect.getblock(source[start:]))
        code = textwrap.dedent(func_code)
        logg.debug("inspecting function\n %s", code)
        func_def = ast.parse(code).body[0]
        decorator_args = func_def.decorator_list[0].args
        # get condition from decorator if present, else None
        condition = None
        if len(decorator_args) > 1:
            cond = decorator_args[1]
            if isinstance(cond, ast.Name):
                condition = cond.id
            elif isinstance(cond, ast.Lambda):
                # extract lambda condition, ugly source hackery ;)
                condition = source[start].strip()[cond.body.col_offset:].rstrip("),")
        last_stmt = func_def.body[-1]
        if isinstance(last_stmt, ast.Return):
            return_value = last_stmt.value
        else:
            return None, condition
        if isinstance(return_value, ast.Tuple):
            state_change = return_value.elts[0]
        else:
            state_change = return_value
        expr = ast.Expression(state_change)
        ast.fix_missing_locations(expr)
        cc = compile(expr, "<expr_ast>", "eval")
#         ctx.update(self.states)
        mod = inspect.getmodule(self)
        try:
            change = eval(cc, mod.__dict__, self.states)
        except Exception as e:
            logg.error("failure analyzing handler '%s'. A programming error in your FSM maybe?", h.__name__, exc_info=1)
            logg.error("source was: \n%s", func_code)
            return None, condition
        return change, condition

    def create_graph(self, add_unhandled_case_handlers=False):
        """Create a graphviz graph (pydot) in memory for future graphviz code / image output.
        To render graphviz code or an image see the render_* methods.
        :param add_unhandled_case_handlers: If True, add all @unhandled_case handlers to the image
            (dotted arrows from each to every other state). Can be quite messy...
        """
        def _create_edge(change, src_node, label, style="solid", unhandled=False):
            style = "dashed" if unhandled else "solid"
            if change == Stay or isinstance(change, Stay):
                edge = Edge(src_node, src_node, color="blue", label=label, style=style)
            elif isinstance(change, Goto):
                dest_node = nodes[change.to]
                edge = Edge(src_node, dest_node, color="black", label=label, style=style)
            elif change == Stop or isinstance(change, Stop):
                stop = nodes[End]
                edge = Edge(src_node, stop, color="red", label=label, style=style)
            else:
                raise Exception("??! " + str(change))
            g.add_edge(edge)

        name = self.__class__.__name__
        g = Dot(graph_name=name,
                    labelloc="t", label="FSM: " + name, fontsize=18, fontcolor="blue")
        g.set_node_defaults(shape="ellipse", fontsize=12)
        g.set_edge_defaults(fontsize=13, labeldistance=3)
        nodes = {}
        handled_msg_types_per_state = {}
        for state in itervalues(self.states):
            if state == self.initial_state:
                color = "green"
            elif state == End:
                color = "red"
            else:
                color = "black"
            node = Node(state.name, color=color, style="rounded", shape="box")
            nodes[state] = node
            g.add_node(node)

        for src_state, src_node in iteritems(nodes):
            for msg_type, h_for_msg_type in iteritems(src_state.handlers):
                for h in h_for_msg_type:
                    change, condition = self._analyze_handler(h)
                    if condition:
                        label = " " + msg_type.__name__ + ": " + condition + " "
                    else:
                        label = " " + msg_type.__name__ + " "
                        # collect msg types which are finally handled by this state
                        handled_msg_types_per_state.setdefault(src_state, []).append(msg_type)
                    _create_edge(change, src_node, label)

        if add_unhandled_case_handlers:
            for msg_type, h_for_msg_type in iteritems(self.handlers):
                for h in h_for_msg_type:
                    change, condition = self._analyze_handler(h)
                    if change:
                        for src_state, src_node in iteritems(nodes):
                            if msg_type not in handled_msg_types_per_state.get(src_state, []):
                                _create_edge(change, src_node, msg_type.__name__, unhandled=True)
        self._graph = g

    @classmethod
    def generate_state_assignments(cls):
        TMPL = "{state} = {fsm}.{state}"
        lines = []
        for state_name in cls.states:
            lines.append(TMPL.format(fsm=cls.__name__, state=state_name))
        return "\n".join(lines)

    def render_dot(self, filepath):
        """Output graphviz code to `filepath`"""
        self._graph.write_raw(filepath)

    def render_svg(self, filepath):
        """Output svg code to `filepath`"""
        self._graph.write_svg(filepath)

    def render_png(self, filepath):
        """Output png image to `filepath`"""
        self._graph.write_png(filepath)

    def dot(self):
        """Get graphviz code."""
        return self._graph.to_string()

    @property
    def accepted_messages(self):
        """Gets messages which would be accepted in the current state (including @unhandled_case handlers).
        """
        return set(chain(iterkeys(self.state.handlers), iterkeys(self.handlers)))

    @property
    def accepted_messages_all_states(self):
        """Gets all messages which would be accepted in some state (or in a @unhandled_case handler).
        """
        accepted = []
        for state in itervalues(self.states):
            accepted.append(iterkeys(state.handlers))
        return set(chain(*accepted))

    @property
    def stopped(self):
        """Are we in the End state?"""
        return self.state is End

    def call(self, func, *args, **kwargs):
        """Call `func` with current state and state data as first arguments.
        *args and **kwargs are passed to `func`.
        """
        return func(self.state, self.data, *args, **kwargs)

    def action(self, *args, **kwargs):
        """Run action for current state with state and state data as first arguments.
        Results are returned. See `State.set_action()`"""
        return self.state.action(self.state, self.data, *args, **kwargs)


    def __eq__(self, other):
        return (self.name == other.name and
            self.state == other.state and
            self.data == other.data)


    def __hash__(self):
        return hash((self.name, self.state, self.name))

### state method decorators

def case(message_type, condition=None, pos=sys.maxsize):
    """
    Marks a static method in a State subclass as transition handler.
    The @staticmethod decorator doesn't have to be specified, this @case decorator handles that for you.
    :param message_type: Only messages with type `message_type` are matched by this handler.
    :param condition: Callable which is called with the message and current data as arguments.
        Returned truth value decides if handler matches.
    :param pos: Try to match this handler before every other handler with `pos`(other) > `pos`.
        If handlers have the same `pos`, the following rules apply:
        * handlers with condition are matched before handlers without
        * handlers which are defined earlier in the state class (lower line number) are matched first
    """

    def _case(f):
        f._message_type = message_type
        f._bound_to_state = True
        f._condition = condition
        f._pos = pos
        return staticmethod(f)
    return _case


def unhandled_case(message_type, condition=None, pos=sys.maxsize):
    """
    Marks a static method in a FSM subclass as transition handler for unhandled messages.
    These handlers are only tried if no handler in the current state matches.
    The @staticmethod decorator doesn't have to be specified, this @case decorator handles that for you.
    :param message_type: Only messages with type `message_type` are matched by this handler.
    :param condition: Callable which is called with the message and current data as arguments.
        Returned truth value decides if handler matches.
    :param pos: Try to match this handler before every other handler with `pos`(other) > `pos`.
        If handlers have the same `pos`, the following rules apply:
        * handlers with condition are matched before handlers without
        * handlers which are defined earlier in the state class (lower line number) are matched first
    """
    def _unhandled_case(f):
        f._message_type = message_type
        f._condition = condition
        f._bound_to_state = False
        f._pos = pos
        return staticmethod(f)
    return _unhandled_case


def on_transition(src_state, dest_state):
    """Marks a static method in a FSM subclass as transition action. These actions are called if the specified transition occurs.
    Returning Stay from a handler method doesn't call any actions.
    :param src_state: name of the State subclass before the transition or the State class itself to match all states
    :type src_state: str
    :param dest_state: Same as src_state for the new state. "End" can be given to match transitions to the End state (i.e. handler returned Stop)
    """
    def _on_transition(f):
        f._src_state = src_state
        f._dest_state = dest_state
        return staticmethod(f)
    return _on_transition