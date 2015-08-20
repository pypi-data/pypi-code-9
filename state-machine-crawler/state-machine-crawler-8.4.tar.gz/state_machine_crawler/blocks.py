import inspect

from abc import ABCMeta, abstractmethod

from .errors import DeclarationError


def transition(source_state=None, target_state=None, cost=1):
    """

    A decorator that represents a process of moving from source_state to target_state

    cost (int)
        Relative *price* of the transition. Transitions that take longer time to run are more *expensive*. The *cost*
        has to be experimentally determined.
    target_state (subclass of :class:`State <state_machine_crawler.State>` or string "self")
        The state to which the system should be transitioned, if "self" is used the transition is done to the holder
        class itself
    source_state (subclass of :class:`State <state_machine_crawler.State>`)
        The state from which the system should be transitioned

    The only difference between *target_state* and *source_state* is a direction of the relationship.

    Note: there can be only *target_state* or only *source_state* because if a transition from state **A** to state
    **B** is possible it does not at all imply that the opposite transition can be performed the same way.

    It is also possible to use string values for *source_state* or *target_state* in conjunction with
    :class:`StateCollections <state_machine_crawler.StateCollection>` subclass
    to define the entry points.

    Sample usage:

    .. code:: python

        class ParentState(State):

            ...


        class YourState(State):

            ...

            @transition(source_state=ParentState)
            def come_from_parent(self):
                ...

            @transition(target_state=ParentState, cost=3)
            def go_to_parent(self):
                ...

    """

    def wrap(function):
        def wraped_f(state_instance):
            function(state_instance)
        wraped_f.source_state = source_state
        wraped_f.target_state = target_state
        wraped_f.cost = cost
        wraped_f.original = getattr(wraped_f, "original", function)
        setattr(wraped_f, "@transition@", True)
        return wraped_f

    return wrap


class StateMetaClass(ABCMeta):

    def __str__(self):
        return "$|{0}".format(self.full_name)

    def __init__(self, name, bases, attrs):
        super(StateMetaClass, self).__init__(name, bases, attrs)
        self.incoming = []
        self.outgoing = []
        self.transitions = []
        self.with_placeholders = False
        self.full_name = self.__module__ + "." + self.__name__

        for name in dir(self):
            attr = getattr(self, name)

            if not hasattr(attr, "@transition@"):
                continue

            self.transitions.append(attr)
            target = attr.target_state
            source = attr.source_state

            if target == "self":
                target = self

            def _ver(item):
                if isinstance(item, basestring):
                    return False
                return item and item.__name__.startswith("_")

            if _ver(target) or _ver(self) or _ver(source):
                continue

            if source and target:
                raise DeclarationError("Only target or source state can be defined for %r " % attr)
            elif target:
                self.outgoing.append(target)
            elif source:
                self.incoming.append(source)
            else:
                raise DeclarationError("No target nor source state is defined for %r" % attr)

            if isinstance(attr.target_state, basestring) and attr.target_state != "self":
                self.with_placeholders = True

            if isinstance(attr.source_state, basestring):
                self.with_placeholders = True


class State(object):
    """ A base class for any state of the system

    States have a *_system* attribute that represents a `SUT <http://xunitpatterns.com/SUT.html>`_.
    """
    __metaclass__ = StateMetaClass

    def __init__(self, system):
        self._system = system

    @abstractmethod
    def verify(self):
        """
        Checks if the system ended up in a desired state. Should raise an exception (e.g. using 'assert' statement) if
        something is not valid
        """

    @classmethod
    def copy(cls, transition_map):
        """
        Creates a copy of a class with transition sources / targets being substituted with the state from the
        map.

        transition_map (dict)
            a mapping between:

            key (string)
                transition name

            value (subclass of :class:`State <state_machine_crawler.State>`)
                substitution for transition's source/target

        return (subclass of :class:`State <state_machine_crawler.State>`)
            State's copy

        .. code:: python

            ...

            StateCopy = ParentState.copy({
                "move_in": NewSourceState,
                "move_out": NewTargetState
            })


        """

        class NewClass(cls):
            pass

        for transition_name, state in transition_map.iteritems():
            original = getattr(NewClass, transition_name, None)
            if not original or not hasattr(original, "@transition@"):
                raise DeclarationError("Transition %r does not exist in %r" % (transition_name, cls.__name__))

            if not inspect.isclass(state) or not issubclass(state, State):
                raise DeclarationError("State for transition %r in %r must be a State subclass" % (
                                       transition_name, cls.__name__))

            if original.source_state:
                NewClass.incoming.remove(original.source_state)
                new_call = transition(source_state=state)(original)
                NewClass.incoming.append(state)
            else:
                NewClass.outgoing.remove(original.target_state)
                new_call = transition(target_state=state)(original)
                NewClass.outgoing.append(state)

            setattr(NewClass, transition_name, new_call)

        setattr(NewClass, "@copy@", True)

        return NewClass
