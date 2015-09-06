# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import inspect

from _Details.Mock import Mock
from _Details.ExpectationGrouping import OrderedExpectationGroup, UnorderedExpectationGroup, AtomicExpectationGroup, OptionalExpectationGroup, AlternativeExpectationGroup, RepeatedExpectationGroup
from _Details.ExpectationHandler import ExpectationHandler


class Engine:
    def __init__(self):
        self.__handler = ExpectationHandler(OrderedExpectationGroup())
        self.__replaced = []

    def create(self, name):
        return Mock(name, self.__handler)

    def replace(self, name):  # @todo Add optional param to pass the mock in (to allow replacing several things by same mock)
        container, attribute = self.__findByName(name)
        self.__replaced.append((container, attribute, getattr(container, attribute)))
        m = self.create(name)
        setattr(container, attribute, m.object)
        return m

    @staticmethod
    def __findByName(name):
        names = name.split(".")
        attribute = names[-1]
        current = inspect.currentframe()
        try:
            frame = current.f_back.f_back
            symbols = dict(frame.f_globals)
            symbols.update(frame.f_locals)
            container = symbols[names[0]]
        finally:
            del current
        for name in names[1:-1]:
            container = getattr(container, name)
        return container, attribute

    def tearDown(self):
        for container, attribute, value in self.__replaced:
            setattr(container, attribute, value)
        self.__handler.tearDown()

    @property
    def unordered(self):
        return self.__handler.pushGroup(UnorderedExpectationGroup())

    @property
    def ordered(self):
        return self.__handler.pushGroup(OrderedExpectationGroup())

    @property
    def atomic(self):
        return self.__handler.pushGroup(AtomicExpectationGroup())

    @property
    def optional(self):
        return self.__handler.pushGroup(OptionalExpectationGroup())

    @property
    def alternative(self):
        return self.__handler.pushGroup(AlternativeExpectationGroup())

    @property
    def repeated(self):
        return self.__handler.pushGroup(RepeatedExpectationGroup())

    @property
    def records(self):
        return self.__handler.getRecordedCalls()
