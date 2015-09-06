# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class Equality:
    def __init__(self, args, kwds):
        self.__args = args
        self.__kwds = kwds

    def __call__(self, args, kwds):
        # @todo Test this optimization (it avoids calling __eq__, which is good for example when expecting... a mock.object)
        return (
            kwds == self.__kwds
            and len(args) == len(self.__args)
            and all((a is b or a == b) for (a, b) in zip(args, self.__args))
        )
