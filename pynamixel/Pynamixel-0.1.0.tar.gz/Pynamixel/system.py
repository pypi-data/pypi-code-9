# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import contextlib

from .instructions import WriteData, RegWrite, Action


class System(object):
    """
    The main class.
    """
    def __init__(self, bus):
        self.__bus = bus
        self.__devices = {}
        self.__instruction_for_writes = [WriteData]

    @property
    def bus(self):
        """
        The :class:`.Bus` instance of the system.
        """
        return self.__bus

    @property
    def instruction_for_writes(self):
        return self.__instruction_for_writes[-1]

    def add_device(self, cls, index):
        """
        Add a device to the system.
        """
        assert index not in self.__devices
        device = cls(self, index)
        self.__devices[index] = device
        return device

    def get_device(self, index):
        """
        Get a device previously added with :meth:`.add_device`.
        """
        return self.__devices[index]

    @property
    @contextlib.contextmanager
    def registered_writes(self):
        """
        Context manager telling the system to use :class:`.RegWrite` to perform registered writes and send an :class:`.Action` instruction at the end.
        See also :attr:`.direct_writes` to temporarily restore direct writes.

        @todoc Add a section about registered writes in the user guide, and how beautiful it is to be able to re-use the code written for direct writes.
        """
        self.__instruction_for_writes.append(RegWrite)
        yield
        self.__bus.broadcast(Action())
        self.__instruction_for_writes.pop()

    @property
    @contextlib.contextmanager
    def direct_writes(self):
        """
        Context manager telling the system to use :class:`.WriteData` to perform direct writes.
        This is the default behaviour and is usefull only when nested in a :attr:`.registered_writes` context manager.
        """
        self.__instruction_for_writes.append(WriteData)
        yield
        self.__instruction_for_writes.pop()
