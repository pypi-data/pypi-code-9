# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class Mock(object):
    def __init__(self, name, handler):
        self.__name = name
        self.__handler = handler

    @property
    def expect(self):
        return self.__handler.expect(self.__name)

    @property
    def object(self):
        return self.__handler.object(self.__name)

    def record(self, realObject):
        # @todo In record mode, catch exceptions. Funny: there is not always a "return" key in getRecordedCalls
        return self.__handler.record(self.__name, realObject)
