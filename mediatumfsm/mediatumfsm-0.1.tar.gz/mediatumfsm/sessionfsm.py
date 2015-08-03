# -*- coding: utf-8 -*-
from copy import copy
from mediatumfsm.fsm import FSM


class SessionFSM(FSM):
    """FSM which saves its current state to a Session (from Flask, for example)"""
    # fields which will be ignored when saving current state data
    # can be used for transient caching fields etc.
    ignored_data_fields = None
    # must be set by subclass to an object like werkzeug.LocalProxy which proxies a dict-like object
    session = None

    def save_state(self):
        """Saves the current state and associated state data.
        Fields in self.ignored_data_fields are skipped.
        """
        if self.name is not None:
            self.session.setdefault(self.name, {})
            o = self.session[self.name]
        else:
            o = self.session
        o["current_state"] = self.state.__name__
        if self.ignored_data_fields:
            state_data = copy(self.data)
            for field in self.ignored_data_fields:
                try:
                    del state_data.__dict__[field]
                except KeyError:
                    pass
                except AttributeError:
                    break
            o["state_data"] = state_data
        else:
            o["state_data"] = self.data

    @classmethod
    def from_saved_state(cls, name=None):
        """Restore FSM object from saved data
        :param name: name(space) of the FSM, needed when multiple FSM should coexist in one session
        """
        if name is not None:
            o = cls.session.get(name, {})
        else:
            o = cls.session
        return cls(o.get("current_state"), o.get("state_data"), name=name)

    def clear(self):
        """Removes saved state from session"""
        if self.name is not None:
            self.session.setdefault(self.name, {})
            o = self.session[self.name]
        else:
            o = self.session
        if "current_state" in o:
            del o["current_state"]
        if "state_data" in o:
            del o["state_data"]


    def reset(self):
        """Clears session state and calls FSM reset"""
        self.clear()
        super(SessionFSM, self).reset()
